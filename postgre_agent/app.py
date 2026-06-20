
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
import os
import re

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool



# Below is the configuration of the program, you specify the DB URI in the .env file.

DB_URI = os.getenv("DATABASE_URI")

MODEL_NAME = "gpt-4o-mini"


# Creating the reference to the database using SQLDatabase from LangChain.

db = SQLDatabase.from_uri(DB_URI)


# Creating the language model instance using the imported ChatOpenAI from LangChain.

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0
)


# Block non-select statements.

FORBIDDEN_SQL_KEYWORDS = {
    "insert", "update", "delete",
    "drop", "alter", "truncate",
    "create", "grant", "revoke"
}


def is_safe_sql(query: str) -> bool:
    """
    Allow only SELECT queries.
    Block destructive SQL.
    """
    # Normalize query for checking
    q = query.strip().lower()

    ### 
    # Two checks are below, one to ensure the string starts with SELECT,
    # While the second check is based on the fact that we are passing a string.
    # So it is possible to have this (Select * from users; drop table users) which is a valid string but 
    # it is not what we want to allow.
    ###
    if not q.startswith("select"):
        return False

    return not any(
        re.search(rf"\b{kw}\b", q)
        for kw in FORBIDDEN_SQL_KEYWORDS
    )


# =========================
# TOOL WRAPPING
# =========================

def create_safe_sql_tool(original_tool):
    """
    Wrap SQL tool to enforce safety rules.
    """

    def safe_sql_executor(query: str):
        print(f"🔍 SQL Query Attempt:\n{query}")

        if not is_safe_sql(query):
            return "❌ Blocked: Only safe SELECT queries are allowed."

        return original_tool.invoke(query)

    return safe_sql_executor


def build_tools():
    """
    Build SQL tools and wrap only query tool safely.
    """
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    safe_tools = []

    for tool in tools:
        if tool.name == "sql_db_query":
            safe_tools.append(
                Tool(
                    name=tool.name,
                    description=tool.description,
                    func=create_safe_sql_tool(tool),
                )
            )
        else:
            safe_tools.append(tool)

    return safe_tools


tools = build_tools()


# =========================
# AGENT
# =========================

agent = create_react_agent(
    model=llm,
    tools=tools
)


# =========================
# CHAT LOGIC
# =========================

async def chat(message, history):
    """
    Convert Gradio chat history → LangGraph format,
    then call agent.
    """

    messages = []

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    result = await agent.ainvoke({"messages": messages})

    return result["messages"][-1].content


# =========================
# UI
# =========================

demo = gr.ChatInterface(
    fn=chat,
    title="LangGraph PostgreSQL Agent (Clean Version)",
    description="Ask questions about your PostgreSQL database safely using LangGraph.",
    examples=[
        "Show all tables",
        "What columns are in the users table?",
        "How many rows are in each table?"
    ],
    cache_examples=False
)


# =========================
# 9. RUN APP
# =========================

if __name__ == "__main__":
    demo.launch()