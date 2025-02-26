import psycopg2
from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from ..helpers import prompt_helper as helper

api_key = "AIzaSyBq2_GdMf0KhowSVSb0hn4Z_8B81kBewXY"
os.environ["GOOGLE_API_KEY"] = api_key


def generate_sql_from_query_gemini(natural_language_query, table_schema):
    try:
        prompt = helper.get_prompt_to_generate_sql_query(natural_language_query, table_schema)
        print(prompt)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        response = llm.invoke(prompt).content
        print(response)
        return response
    except Exception as e:
        print(f"Error generating SQL: {e}")
    return None


def validate_sql(sql_query, allowed_operations=("SELECT", "ORDER BY", "LIMIT", "WHERE")):
    sql_upper = sql_query.upper()
    for operation in allowed_operations:
        if operation not in sql_upper:
            if "SELECT" not in allowed_operations or sql_upper.find("SELECT") != 0:
                return False
    if "INSERT" in sql_upper or "UPDATE" in sql_upper or "DELETE" in sql_upper or "DROP" in sql_upper or "ALTER" in sql_upper:
        return False
    return True


def execute_sql_query(sql_query):
    if not validate_sql(sql_query):
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
        return results, column_names
    except psycopg2.Error as e:
        return f"Database error: {e}"
    except Exception as e:
        return f"Error executing query: {e}"


def get_table_schema(table_name):
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
    return schema
