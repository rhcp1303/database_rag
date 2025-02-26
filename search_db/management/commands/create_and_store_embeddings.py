from django.core.management.base import BaseCommand
from search_db.models import Departments, Employees, Orders, Products
from ...helpers import create_and_store_embeddings_helper as helper


class Command(BaseCommand):
    help = 'Generates vector embeddings for text fields in the database'

    def handle(self, *args, **options):

        for dept in Departments.objects.all():
            helper.generate_and_store_embedding(dept, 'name', 'name_embedding')
        for emp in Employees.objects.all():
            helper.generate_and_store_embedding(emp, 'name', 'name_embedding')
            helper.generate_and_store_embedding(emp, 'email', 'email_embedding')
        for order in Orders.objects.all():
            helper.generate_and_store_embedding(order, 'customer_name', 'customer_name_embedding')
        for product in Products.objects.all():
            helper.generate_and_store_embedding(product, 'name', 'name_embedding')
        self.stdout.write(self.style.SUCCESS('Embeddings generated successfully!'))
