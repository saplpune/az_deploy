from django.db import models

# Create your models here.

class SalesData(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

class InventoryData(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class HRData(models.Model):
    department = models.CharField(max_length=255)
    employee_count = models.IntegerField()

class DashboardCache(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    current_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold')
    ])
    progress = models.IntegerField(default=0)  # Add default value if needed

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    hire_date = models.DateField()

class ProductionData(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    efficiency = models.FloatField()

class QualityControlData(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    defects = models.IntegerField()

class MachineData(models.Model):
    machine_id = models.CharField(max_length=50)
    uptime = models.FloatField()
    downtime = models.FloatField()

class SupplyChainData(models.Model):
    date = models.DateField()
    supplier = models.CharField(max_length=100)
    lead_time = models.IntegerField()

class CustomerSatisfactionData(models.Model):
    date = models.DateField()
    customer = models.CharField(max_length=100)
    satisfaction_score = models.IntegerField()

class EnergyConsumptionData(models.Model):
    date = models.DateField()
    consumption = models.FloatField()

class MaintenanceData(models.Model):
    date = models.DateField()
    machine_id = models.CharField(max_length=50)
    maintenance_type = models.CharField(max_length=50)
    duration = models.FloatField()

class RDProjectData(models.Model):
    project_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    progress = models.FloatField()
