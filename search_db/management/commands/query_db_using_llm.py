import logging
from django.core.management.base import BaseCommand
from ...helpers import query_db_using_llm_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Perform natural language query over database using LLM'

    def handle(self, *args, **options):
        """
        Performs a natural language query over the database using a Large Language Model (LLM).

        This command retrieves table schemas, generates an SQL query from a natural language query
        using an LLM, executes the SQL query, and displays the results.

        It logs the generated SQL, query results, and any errors that occur.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None.

        Raises:
            Exception: If any error occurs during the query processing.

        Example:
            To run this command, use:
            `python manage.py natural_language_query`
        """
        try:
            table_name_list = ["employees", "departments", "orders", "products"]
            table_schema_list = [helper.get_table_schema(table_name) for table_name in table_name_list]
            natural_language_query = "show me name of product in orders which are handled by Aarav Sharma"
            sql_query = helper.generate_sql_from_query_gemini(natural_language_query, table_schema_list)

            if sql_query:
                logger.info(f"Generated SQL: {sql_query}")
                results = helper.execute_sql_query(sql_query)

                if isinstance(results, tuple):
                    data, column_names = results
                    logger.info(f"Column Names: {column_names}")
                    logger.info(f"Results: {data}")
                    self.stdout.write(self.style.SUCCESS(f"Column Names: {column_names}"))
                    self.stdout.write(self.style.SUCCESS(f"Results: {data}"))

                else:
                    logger.info(f"Results: {results}")
                    self.stdout.write(self.style.SUCCESS(f"Results: {results}"))

            else:
                logger.error("Failed to generate SQL.")
                self.stdout.write(self.style.ERROR("Failed to generate SQL."))

        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Error processing query: {e}"))