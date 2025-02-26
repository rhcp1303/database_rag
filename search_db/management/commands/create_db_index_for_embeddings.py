from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Creates HNSW indexes on vector embedding columns'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE INDEX products_name_embedding_idx ON products USING hnsw (name_embedding vector_cosine_ops);
                CREATE INDEX orders_customer_name_embedding_idx ON orders USING hnsw (customer_name_embedding vector_cosine_ops);
                CREATE INDEX employees_name_embedding_idx ON employees USING hnsw (name_embedding vector_cosine_ops);
                CREATE INDEX departments_name_embedding_idx ON departments USING hnsw (name_embedding vector_cosine_ops);
                CREATE INDEX employees_email_embedding_idx ON employees USING hnsw (email_embedding vector_cosine_ops);
            """)
        self.stdout.write(self.style.SUCCESS('HNSW indexes created successfully!'))