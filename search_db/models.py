from django.db import models

class Departments(models.Model):
    """Represents a company department."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employees(models.Model):
    """Represents an employee."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Orders(models.Model):
    """Represents a customer order."""
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField()

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class Products(models.Model):
    """Represents a product in the catalog."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name