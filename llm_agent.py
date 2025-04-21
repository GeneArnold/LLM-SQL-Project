import os
from dotenv import load_dotenv
from openai import OpenAI
from query_handler import run_sql_query
import re

# 1. Load API key and init client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Define your schema (could also load this from a .txt file)
schema_description = """
Tables:
customers(id, name, email, signup_date)
orders(id, customer_id, product_type, amount, order_date)
addresses(id, customer_id, street, city, state, zip)

- customers.id = orders.customer_id
- customers.id = addresses.customer_id
- addresses.state uses 2-letter US state abbreviations (e.g., 'TX', 'WI', 'IL')
"""


# 3. Few-shot example: teach the model how to answer
system_prompt = f"""
You are a Postgres SQL expert. Given a question and the database schema below,
generate a syntactically correct SQL query that answers the question.

{schema_description}

Example:
Question: Who has ordered the most books?
SQL:
SELECT c.name, SUM(o.amount) AS total_books
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.product_type = 'book'
GROUP BY c.name
ORDER BY total_books DESC
LIMIT 1;

Example:
Question: Which customers are from Texas and ordered books?
SQL:
SELECT c.name
FROM customers c
JOIN addresses a ON c.id = a.customer_id
JOIN orders o ON c.id = o.customer_id
WHERE a.state = 'TX' AND o.product_type = 'book';

Now respond only with SQL that answers new questions.
"""



# 4. Ask a question
user_question = "Who has ordered the least number of books?"

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
)

def extract_sql_from_response(response_text: str) -> str:
    """
    Extracts the SQL code from an LLM response, removing markdown formatting and text.
    """
    # Remove markdown ```sql blocks
    cleaned = re.sub(r"```sql|```", "", response_text)
    return cleaned.strip()

def generate_sql_from_question(user_question: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
    )
    raw_sql = response.choices[0].message.content
    cleaned_sql = extract_sql_from_response(raw_sql)
    return raw_sql, cleaned_sql


raw_sql = response.choices[0].message.content
sql = extract_sql_from_response(raw_sql)
print("🧠 Cleaned Generated SQL:\n", sql)

print("🧠 Data returned from SQL:")
results = run_sql_query(sql)
print(results)

