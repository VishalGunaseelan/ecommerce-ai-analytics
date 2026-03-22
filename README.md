# E-Commerce AI Analytics — Text-to-SQL on Databricks

Ask questions about e-commerce sales data in plain English 
and get instant answers powered by AI.

🔴 **[Live App](https://ecommerce-ai-analytics-n3q5hbt3p4uogdxgka6sa6.streamlit.app/#e-commerce-ai-analytics)**

---

## What This Does

Type a natural language question like:
> *"Who are the top 5 customers by lifetime value?"*

The app:
1. Converts your question to SQL using Groq LLM + LangChain
2. Runs the query against live Delta tables on Databricks
3. Returns results as an interactive table

---

## Architecture
```
PySpark Pipeline (Databricks)
        ↓
Medallion Architecture (Bronze → Silver → Gold)
        ↓
Star Schema Delta Tables (8 tables)
        ↓
Power BI Dashboard (3 pages)
        ↓
AI Text-to-SQL App (Groq LLM + LangChain + Streamlit)
        ↓
Deployed on Streamlit Cloud
```

---

## Pipeline Features

- **Medallion Architecture** — Bronze (raw), Silver (clean), Gold (aggregated)
- **SCD Type 2** — full history tracking on dimension tables
- **Hash-based MERGE** — incremental change detection
- **Data Quarantine** — invalid records isolated with rejection reasons
- **Audit Logging** — every run tracked with records processed and status
- **OPTIMIZE + ZORDER + VACUUM** — production-grade Delta table maintenance

---

## Gold Layer Tables

| Table | Description |
|---|---|
| fact_orders | All transactions |
| dim_customers | Customer dimension (SCD Type 2) |
| dim_products | Product dimension (SCD Type 2) |
| daily_revenue | Revenue aggregated by date |
| product_revenue | Revenue aggregated by product |
| category_revenue | Revenue aggregated by category |
| customer_kpis | Lifetime value, order count per customer |
| repeat_customers | Customers with more than one order |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Pipeline | PySpark, Delta Lake, Databricks |
| AI / LLM | LangChain, Groq LLM (Llama 3.1) |
| Frontend | Streamlit |
| Visualisation | Power BI |
| Language | Python |
| Version Control | Git, GitHub |

---

## Example Questions to Try

- Who are the top 5 customers by lifetime value?
- What is the total revenue by category?
- Show me daily revenue for January 2025
- Which product has the most orders?
- How many repeat customers are there?

---

## Setup (Local)
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
DATABRICKS_HOST=your-host
DATABRICKS_TOKEN=your-token
HTTP_PATH=your-http-path
GROQ_API_KEY=your-groq-key

# Run
streamlit run DE.py
```

---

## Author

**Vishal Gunaseelan**  
Data Analytics Engineer | IBM Cognos | PySpark | Databricks | Power BI  
[LinkedIn](https://www.linkedin.com/in/vishal-g-20)
