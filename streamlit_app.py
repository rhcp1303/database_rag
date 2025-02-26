import os
import django
from search_db.helpers import query_db_using_llm_helper as helper
import streamlit as st
import pandas as pd
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "database_rag.settings")
django.setup()


def query_db_using_llm(natural_language_query):
    """
    Generates and executes an SQL query based on a natural language query.

    This function takes a natural language query, retrieves table schemas, generates
    an SQL query using a language model, executes the query against the database, and
    returns the results.

    Args:
        natural_language_query (str): The natural language query to convert to SQL.

    Returns:
        tuple or str: A tuple containing the query results (list of tuples) and column names
                     (list of strings), or an error message (str) if the query fails.
    """
    try:
        table_name_list = ["employees", "departments", "orders", "products"]
        table_schema_list = [helper.get_table_schema(table_name) for table_name in table_name_list]
        sql_query = helper.generate_sql_from_query_gemini(natural_language_query, table_schema_list)
        if sql_query:
            logger.debug(f"Generated SQL: {sql_query}")
            results = helper.execute_sql_query(sql_query)
            return results
        else:
            return "Failed to generate SQL."
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return f"An error occurred: {e}"


st.title("Natural Language Search App")
natural_language_query = st.text_area("Enter your natural language query:",
                                      "show me name of products whose orders are handled by Aarav Sharma")

if st.button("Search"):
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
