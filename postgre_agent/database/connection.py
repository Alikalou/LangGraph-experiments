from langchain_community.utilities import SQLDatabase
from config.settings import DATABASE_URI


def get_database():
    return SQLDatabase.from_uri(DATABASE_URI)