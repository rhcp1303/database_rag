def get_prompt_to_generate_sql_query(table_schema_list, natural_language_query):
    prompt = f"""
            Given the following natural language query, generate a valid Postgress SQL query using the provided database
            schemas list
            Database Schema List: {table_schema_list}
            Natural Language Query: {natural_language_query}
            SQL Query: (Return only the SQL query, without any formatting or backticks)
            """

    return prompt
