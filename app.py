import streamlit as st
from llm_agent import generate_sql_from_question
from query_handler import run_sql_query

st.set_page_config(page_title="LLM SQL Assistant", page_icon="🧠")

st.title("🧠 LLM SQL Assistant")
st.markdown("Ask natural language questions about your customer + order data.")

user_question = st.text_input("Enter your question", placeholder="e.g. Who bought the most books?")

if st.button("Submit") and user_question:
    with st.spinner("Thinking... 🤔"):
        # Step 1: Generate SQL from LLM
        raw_sql, cleaned_sql = generate_sql_from_question(user_question)

        # Step 2: Run the SQL
        results = run_sql_query(cleaned_sql)

    st.subheader("🧾 Generated SQL")
    st.code(cleaned_sql, language="sql")

    st.subheader("📊 Query Results")
    if isinstance(results, dict) and "error" in results:
        st.error(f"❌ {results['error']}")
    elif results:
        st.dataframe(results, use_container_width=True)
    else:
        st.info("No results found.")

st.markdown("---")
st.caption("Built with ❤️ by you and ChatGPT. [Blog series coming soon!]")
