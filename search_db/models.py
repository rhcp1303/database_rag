from django.db import models
from django.db.models import FloatField
from pgvector.django import VectorField


class Departments(models.Model):
    """Represents a company department."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'


class Employees(models.Model):
    """Represents an employee."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)
    email_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employees'


class Orders(models.Model):
    """Represents a customer order."""
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField()
    customer_name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    class Meta:
        db_table = 'orders'


class Products(models.Model):
    """Represents a product in the catalog."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
