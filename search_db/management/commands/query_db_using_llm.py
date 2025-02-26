from django.core.management.base import BaseCommand
from ...helpers import query_db_using_llm_helper as helper

class Command(BaseCommand):
    help = 'Perform natural language query over database using LLM'

    def handle(self, *args, **options):
        table_name_list = ["employees", "departments", "orders", "products"]
        table_schema_list = [helper.get_table_schema(table_name) for table_name in table_name_list]
        natural_language_query = "show me name of product in orders which are handled by Aarav Sharma"
        sql_query = helper.generate_sql_from_query_gemini(natural_language_query, table_schema_list)
        if sql_query:
            print(f"Generated SQL: {sql_query}")
            results = helper.execute_sql_query(sql_query)
            if isinstance(results, tuple):
                data, column_names = results
                print(f"Column Names: {column_names}")
                print(f"Results: {data}")
            else:
                print(results)
        else:
            print("Failed to generate SQL.")
