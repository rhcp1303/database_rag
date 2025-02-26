import psycopg2
from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import logging
from ..helpers import prompt_helper as helper

logger = logging.getLogger(__name__)

api_key = "AIzaSyBq2_GdMf0KhowSVSb0hn4Z_8B81kBewXY"
os.environ["GOOGLE_API_KEY"] = api_key


def generate_sql_from_query_gemini(natural_language_query, table_schema):
    """
    Generates an SQL query from a natural language query using Google's Gemini model.

    This function takes a natural language query and a table schema as input, constructs a prompt,
    and uses the Gemini model to generate an SQL query that corresponds to the natural language query.

    Args:
        natural_language_query (str): The natural language query to convert to SQL.
        table_schema (list): A list of tuples, where each tuple represents a column in the table
                            and contains the column name and data type.

    Returns:
        str: The generated SQL query, or None if an error occurs.

    Raises:
        Exception: If there's an error during prompt construction or interaction with the Gemini API.

    Example:
        ```python
        natural_language_query = "Show me the names of all employees in the sales department."
        table_schema = [("employee_id", "integer"), ("employee_name", "varchar"), ("department", "varchar")]
        sql_query = generate_sql_from_query_gemini(natural_language_query, table_schema)
        if sql_query:
            print(sql_query)
        ```
    """
    try:
        prompt = helper.get_prompt_to_generate_sql_query(natural_language_query, table_schema)
        logger.debug(f"Generated prompt: {prompt}")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        response = llm.invoke(prompt).content
        logger.debug(f"Gemini response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error generating SQL: {e}", exc_info=True)
        return None


def validate_sql(sql_query, allowed_operations=("SELECT", "ORDER BY", "LIMIT", "WHERE")):
    """
    Validates an SQL query against a list of allowed operations.

    This function checks if the provided SQL query contains only the allowed operations and does not
    contain any potentially harmful operations like INSERT, UPDATE, DELETE, DROP, or ALTER.

    Args:
        sql_query (str): The SQL query to validate.
        allowed_operations (tuple, optional): A tuple of allowed SQL operations. Defaults to
                                                ("SELECT", "ORDER BY", "LIMIT", "WHERE").

    Returns:
        bool: True if the SQL query is valid, False otherwise.

    Example:
        ```python
        sql_query = "SELECT * FROM employees WHERE department = 'sales';"
        is_valid = validate_sql(sql_query)
        print(is_valid)  # Output: True
        ```
    """
    sql_upper = sql_query.upper()
    for operation in allowed_operations:
        if operation not in sql_upper:
            if "SELECT" not in allowed_operations or sql_upper.find("SELECT") != 0:
                return False
    if "INSERT" in sql_upper or "UPDATE" in sql_upper or "DELETE" in sql_upper or "DROP" in sql_upper or "ALTER" in sql_upper:
        return False
    return True


def execute_sql_query(sql_query):
    """
    Executes an SQL query against a PostgreSQL database.

    This function validates the provided SQL query, connects to the database using Django settings,
    executes the query, and returns the results along with column names.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        tuple: A tuple containing the query results (list of tuples) and column names (list of strings),
               or a string error message if the query is invalid or an error occurs.

    Raises:
        psycopg2.Error: If a database error occurs.
        Exception: If any other error occurs during query execution.

    Example:
        ```python
        sql_query = "SELECT employee_name FROM employees WHERE department = 'sales';"
        results = execute_sql_query(sql_query)
        if isinstance(results, tuple):
            data, columns = results
            print(columns)
            for row in data:
                print(row)
        else:
            print(results)
        ```
    """
    if not validate_sql(sql_query):
        logger.warning(f"Invalid SQL query: {sql_query}")
        return "Invalid SQL query."
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        logger.debug(f"Successfully executed query: {sql_query}")
        return results, column_names
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}", exc_info=True)
        return f"Database error: {e}"
    except Exception as e:
        logger.error(f"Error executing query: {e}", exc_info=True)
        return f"Error executing query: {e}"


def get_table_schema(table_name):
    """
    Retrieves the schema of a specified table from a PostgreSQL database.

    This function connects to the database using Django settings and retrieves the column names
    and data types for the given table.

    Args:
        table_name (str): The name of the table to retrieve the schema for.

    Returns:
        list: A list of tuples, where each tuple contains the column name and data type,
              or None if an error occurs.

    Raises:
        psycopg2.Error: If a database error occurs.
        Exception: If any other error occurs during query execution.

    Example:
        ```python
        table_name = "employees"
        schema = get_table_schema(table_name)
        if schema:
            for column, data_type in schema:
                print(f"{column}: {data_type}")
        ```
    """
    try:
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """)
        schema = cursor.fetchall()
        conn.close()
        logger.debug(f"Retrieved schema for table: {table_name}")
        return schema
    except psycopg2.Error as e:
        logger.error(f"Database error retrieving schema: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error retrieving schema: {e}", exc_info=True)
        return None