from config.settings import OPENAI_MODEL, DATABASE_URI

from database.connection import get_database

from tools.sql_tools import build_tools

from agent.builder import build_agent

from langchain_openai import ChatOpenAI

from ui.chat import chat_interface


# =========================
# 1. LLM
# =========================

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0
)


# =========================
# 2. DATABASE
# =========================

db = get_database()


# =========================
# 3. TOOLS
# =========================

tools = build_tools(db=db, llm=llm)


# =========================
# 4. AGENT
# =========================

agent = build_agent(model=llm, tools=tools)


# =========================
# 5. UI
# =========================

demo = chat_interface(agent)


# =========================
# 6. RUN APP
# =========================

if __name__ == "__main__":
    demo.launch()