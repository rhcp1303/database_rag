import os
import django
from search_db.helpers import query_db_using_llm_helper as helper
import streamlit as st
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "database_rag.settings")
django.setup()


def query_db_using_llm(natural_language_query):
    table_name_list = ["employees", "departments", "orders", "products"]
    table_schema_list = [helper.get_table_schema(table_name) for table_name in table_name_list]
    sql_query = helper.generate_sql_from_query_gemini(natural_language_query, table_schema_list)
    if sql_query:
        print(f"Generated SQL: {sql_query}")
        results = helper.execute_sql_query(sql_query)
        return results
    else:
        return "Failed to generate SQL."


st.title("Natural Language to SQL Query")
natural_language_query = st.text_area("Enter your natural language query:",
                                      "show me name of products whose orders are handled by Aarav Sharma")
if st.button("Generate and Execute SQL"):
    if natural_language_query:
        results = query_db_using_llm(natural_language_query)
        if isinstance(results, str):
            st.error(results)
        elif isinstance(results, tuple):
            data, column_names = results
            df = pd.DataFrame(data, columns=column_names, index=range(1, len(data) + 1))
            st.dataframe(df)
        else:
            st.write("An unexpected error occurred.")
    else:
        st.warning("Please enter a query.")
