from langchain_community.agent_toolkits import SQLDatabaseToolkit

from tools.safe_sql_tool import create_safe_sql_tool

def build_tools(db, llm):

    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )

    tools = []

    for tool in toolkit.get_tools():

        if tool.name == "sql_db_query":
            tools.append(
                create_safe_sql_tool(tool)
            )
        else:
            tools.append(tool)

    return tools


