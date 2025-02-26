import logging
from django.core.management.base import BaseCommand
from search_db.models import Departments, Employees, Orders, Products
from ...helpers import create_and_store_embeddings_helper as helper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generates vector embeddings for text fields in the database'

    def handle(self, *args, **options):
        """
        Generates and stores vector embeddings for text fields in the database models.

        This command iterates through all instances of Departments, Employees, Orders, and Products models,
        generates embeddings for specified text fields using the `generate_and_store_embedding` helper function,
        and stores the embeddings back into the respective model instances.

        It logs the progress and success of the embedding generation process.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        Returns:
            None.

        Raises:
            Exception: If any error occurs during the embedding generation or saving process.

        Example:
            To run this command, use:
            `python manage.py generate_embeddings`
        """
        try:
            for dept in Departments.objects.all():
                helper.generate_and_store_embedding(dept, 'name', 'name_embedding')
                logger.debug(f"Generated embedding for Department: {dept.name}")

            for emp in Employees.objects.all():
                helper.generate_and_store_embedding(emp, 'name', 'name_embedding')
                logger.debug(f"Generated embedding for Employee name: {emp.name}")
                helper.generate_and_store_embedding(emp, 'email', 'email_embedding')
                logger.debug(f"Generated embedding for Employee email: {emp.email}")

            for order in Orders.objects.all():
                helper.generate_and_store_embedding(order, 'customer_name', 'customer_name_embedding')
                logger.debug(f"Generated embedding for Order customer_name: {order.customer_name}")

            for product in Products.objects.all():
                helper.generate_and_store_embedding(product, 'name', 'name_embedding')
                logger.debug(f"Generated embedding for Product name: {product.name}")

            self.stdout.write(self.style.SUCCESS('Embeddings generated successfully!'))
            logger.info("Embeddings generated successfully!")

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"Error generating embeddings: {e}"))
