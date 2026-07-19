import pyodbc

# SQL Server接続情報
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=KnowledgeDB;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)


def get_connection():
    """
    SQL Serverへの接続を取得する
    """
    return pyodbc.connect(CONNECTION_STRING)