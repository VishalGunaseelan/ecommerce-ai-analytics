import streamlit as st
from databricks import sql
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import pandas as pd
from dotenv import load_dotenv
import os

# ── CONFIG ──────────────────────────────────────────
load_dotenv()

DATABRICKS_HOST  = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
HTTP_PATH        = os.getenv("HTTP_PATH")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")



# ── SCHEMA CONTEXT FOR GEMINI ───────────────────────
SCHEMA_CONTEXT = """
You are a SQL expert. Generate only a valid SQL query — no explanation, no markdown, no backticks.

IMPORTANT: Always use fully qualified table names with catalog and schema. Example: workspace.gold.product_revenue

AGGREGATION TABLES (no is_current column — never filter by is_current):
- workspace.gold.product_revenue(product_id INT, product_name STRING, category STRING, total_revenue DOUBLE, total_orders INT, avg_order_value DOUBLE, total_units_sold INT)
- workspace.gold.category_revenue(category STRING, category_revenue DOUBLE, total_orders INT, avg_order_value DOUBLE)
- workspace.gold.daily_revenue(order_date DATE, daily_revenue DOUBLE, total_orders INT, unique_customers INT)
- workspace.gold.customer_kpis(customer_id INT, name STRING, city STRING, lifetime_value DOUBLE, total_orders INT, avg_order_value DOUBLE, last_order_date DATE)
- workspace.gold.repeat_customers(customer_id INT, name STRING, city STRING, order_count INT)
- workspace.gold.fact_orders(order_id INT, customer_id INT, product_id INT, order_date DATE, quantity INT, price DOUBLE, total_amount DOUBLE)

DIMENSION TABLES (these have is_current — always filter WHERE is_current = true):
- workspace.gold.dim_customers(customer_id INT, name STRING, city STRING, is_current BOOLEAN)
- workspace.gold.dim_products(product_id INT, product_name STRING, category STRING, price DOUBLE, is_current BOOLEAN)

Rules:
- ALWAYS prefix every table with workspace.gold. — never use short names
- For top products by sales → use workspace.gold.product_revenue, ORDER BY total_revenue DESC
- For top customers → use workspace.gold.customer_kpis, ORDER BY lifetime_value DESC
- For revenue by category → use workspace.gold.category_revenue
- Always SELECT descriptive columns like names, not just IDs
- Return only the SQL query, nothing else
"""
# ── QUERY DATABRICKS ────────────────────────────────
def run_query(sql_query):
    with sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=HTTP_PATH,
        access_token=DATABRICKS_TOKEN
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cols = [d[0] for d in cursor.description]
            return pd.DataFrame(result, columns=cols)

# ── GENERATE SQL WITH GEMINI ─────────────────────────
def generate_sql(question):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY
    )
    response = llm.invoke([HumanMessage(content=f"{SCHEMA_CONTEXT}\n\nQuestion: {question}")])
    return response.content.strip()
   

# ── STREAMLIT UI ─────────────────────────────────────
st.set_page_config(page_title="E-Commerce AI Analytics", page_icon="📊", layout="wide")

st.title("📊 E-Commerce AI Analytics")
st.caption("Ask questions about your sales data in plain English")

# Example questions
with st.expander("💡 Example questions"):
    st.markdown("""
    - Who are the top 5 customers by lifetime value?
    - What is the total revenue by category?
    - Show me daily revenue for January 2025
    - Which product has the most orders?
    - How many repeat customers are there?
    """)

question = st.text_input("Ask a question about your data:", placeholder="e.g. Show me top 5 customers by revenue")

if st.button("Run", type="primary") and question:
    with st.spinner("Generating SQL..."):
        try:
            sql_query = generate_sql(question)
            st.subheader("Generated SQL")
            st.code(sql_query, language="sql")

            with st.spinner("Querying Databricks..."):
                df = run_query(sql_query)
                st.subheader(f"Results — {len(df)} rows")
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")