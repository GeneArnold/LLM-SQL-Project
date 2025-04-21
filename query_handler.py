import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")

# Build connection string
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def run_sql_query(sql: str):
    """
    Executes the provided SQL query and returns the results as a list of dictionaries.
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text(sql))
            return [dict(row._mapping) for row in result]
        except Exception as e:
            return {"error": str(e)}
