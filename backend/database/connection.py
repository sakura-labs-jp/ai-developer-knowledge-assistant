import os

import pyodbc
from dotenv import load_dotenv


load_dotenv()


DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "KnowledgeDB")


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)


def get_connection():
    """
    Create and return a connection to SQL Server.
    """

    return pyodbc.connect(CONNECTION_STRING)