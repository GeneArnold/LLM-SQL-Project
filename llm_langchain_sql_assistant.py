import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

# Load your Hugging Face token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Init LLM from HF Hub
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.5,              # move this out of model_kwargs
    max_new_tokens=512            # move this out of model_kwargs
)

# Prompt template
prompt_template = PromptTemplate.from_template("""
You are a Postgres SQL expert. Given a question and the schema below,
generate a syntactically correct SQL query. Do not include explanations.

Schema:
customers(id, name, email, signup_date)
orders(id, customer_id, product_type, amount, order_date)
addresses(id, customer_id, street, city, state, zip)

- customers.id = orders.customer_id
- customers.id = addresses.customer_id
- addresses.state uses 2-letter abbreviations (e.g., 'TX', 'WI', 'IL')

Question: {question}

SQL:
""")

# Create a runnable chain
chain = prompt_template | llm

def main():
    user_question = "List all customers who ordered pens and live in Illinois."
    result = chain.invoke({"question": user_question})
    print("Generated SQL:\n", result)

if __name__ == "__main__":
    main()
