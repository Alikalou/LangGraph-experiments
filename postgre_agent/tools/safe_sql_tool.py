from langchain_core.tools import Tool

from database.security import (
    validate_sql,
    enforce_limit,
)


def create_safe_sql_tool(original_tool):

    def run(query: str):

        validate_sql(query)

        query = enforce_limit(query)

        return original_tool.invoke(query)

    return Tool(
        name=original_tool.name,
        description=original_tool.description,
        func=run,
    )