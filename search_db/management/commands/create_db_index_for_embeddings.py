import logging
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates HNSW indexes on vector embedding columns'

    def handle(self, *args, **options):
        """
        Creates HNSW indexes on vector embedding columns in the database.

        This command executes SQL queries to create HNSW indexes on specified vector embedding
        columns in the products, orders, employees, and departments tables. HNSW indexes are used
        for efficient similarity searches on vector data.

        It logs the success or failure of the index creation process.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None.

        Raises:
            Exception: If any error occurs during the index creation process.

        Example:
            To run this command, use:
            `python manage.py create_hnsw_indexes`
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE INDEX products_name_embedding_idx ON products USING hnsw (name_embedding vector_cosine_ops);
                    CREATE INDEX orders_customer_name_embedding_idx ON orders USING hnsw (customer_name_embedding vector_cosine_ops);
                    CREATE INDEX employees_name_embedding_idx ON employees USING hnsw (name_embedding vector_cosine_ops);
                    CREATE INDEX departments_name_embedding_idx ON departments USING hnsw (name_embedding vector_cosine_ops);
                    CREATE INDEX employees_email_embedding_idx ON employees USING hnsw (email_embedding vector_cosine_ops);
                """)
            self.stdout.write(self.style.SUCCESS('HNSW indexes created successfully!'))
            logger.info('HNSW indexes created successfully!')

        except Exception as e:
            logger.error(f"Error creating HNSW indexes: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Error creating HNSW indexes: {e}"))