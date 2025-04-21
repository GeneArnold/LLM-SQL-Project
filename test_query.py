from query_handler import run_sql_query

sql = "SELECT * FROM customers LIMIT 5"
results = run_sql_query(sql)
print(results)
