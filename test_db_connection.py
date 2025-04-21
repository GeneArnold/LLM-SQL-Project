from sqlalchemy import create_engine, inspect, text

# Replace these with your actual DB credentials
DB_USER = 'root'
DB_PASSWORD = 'postgresadmin'
DB_HOST = '192.168.40.51'
DB_PORT = '5432'
DB_NAME = 'llm_project'

# Create the connection string
db_url = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_url)

# Inspect tables
inspector = inspect(engine)
tables = inspector.get_table_names()

print("✅ Connected to the database!")
print("📦 Available tables:")
for table in tables:
    print(f"  - {table}")

# Optional: preview a few rows from each table
with engine.connect() as connection:
    for table in ['customers', 'orders']:
        if table in tables:
            print(f"\n📊 Preview of {table}:")
            result = connection.execute(text(f"SELECT * FROM {table} LIMIT 5"))
            for row in result.mappings():
                print(dict(row))


