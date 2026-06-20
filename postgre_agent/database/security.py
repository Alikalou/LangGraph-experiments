import re
import sqlparse
from sqlparse.tokens import DML

FORBIDDEN = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
}

def validate_sql(query: str) -> None:
    statements = sqlparse.parse(query)

    if len(statements) != 1:
        raise ValueError("Only one statement allowed.")

    stmt = statements[0]
    # A token is the smallest structure in a SQL statement.
    first_token = stmt.token_first(skip_cm=True)

    if (
        first_token is None
        # Check if the token is not a DML, then check if it is not a select statement.
        or first_token.ttype != DML
        or first_token.value.upper() != "SELECT"
    ):
        raise ValueError("Only SELECT queries are allowed.")

    ### Remove the heirarchy and check for forbidden keywords
    for token in stmt.flatten():
        if token.value.upper() in FORBIDDEN:
            raise ValueError(
                f"Forbidden keyword: {token.value}"
            )

def enforce_limit(
    query: str,
    limit: int = 100
) -> str:
    if re.search(
        r"\blimit\b",
        query,
        re.IGNORECASE
    ):
        return query

    query = query.rstrip().rstrip(";")

    return f"{query} LIMIT {limit}"