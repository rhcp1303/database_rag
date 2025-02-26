import logging
from django.db import models
from pgvector.django import VectorField

logger = logging.getLogger(__name__)


class Departments(models.Model):
    """
    Represents a company department.

    Attributes:
        id (AutoField): The primary key for the department.
        name (CharField): The name of the department.
        name_embedding (VectorField): Vector embedding of the department name.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        """Returns the name of the department."""
        return self.name

    class Meta:
        db_table = 'departments'


class Employees(models.Model):
    """
    Represents an employee.

    Attributes:
        id (AutoField): The primary key for the employee.
        name (CharField): The name of the employee.
        department (ForeignKey): The department the employee belongs to.
        email (EmailField): The email address of the employee.
        salary (DecimalField): The salary of the employee.
        name_embedding (VectorField): Vector embedding of the employee name.
        email_embedding (VectorField): Vector embedding of the employee email.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey('Departments', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)
    email_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        """Returns the name of the employee."""
        return self.name

    class Meta:
        db_table = 'employees'


class Orders(models.Model):
    """
    Represents a customer order.

    Attributes:
        id (AutoField): The primary key for the order.
        customer_name (CharField): The name of the customer.
        employee (ForeignKey): The employee who handled the order.
        order_total (DecimalField): The total amount of the order.
        order_date (DateField): The date of the order.
        customer_name_embedding (VectorField): Vector embedding of the customer name.
    """
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField()
    customer_name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        """Returns a string representation of the order."""
        return f"Order #{self.id} - {self.customer_name}"

    class Meta:
        db_table = 'orders'


class Products(models.Model):
    """
    Represents a product in the catalog.

    Attributes:
        id (AutoField): The primary key for the product.
        name (CharField): The name of the product.
        price (DecimalField): The price of the product.
        name_embedding (VectorField): Vector embedding of the product name.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        """Returns the name of the product."""
        return self.name

    class Meta:
        db_table = 'products'