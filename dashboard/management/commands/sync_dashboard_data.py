import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from dashboard.models import SalesData, InventoryData, Product, Project, Employee, ProductionData, QualityControlData, MachineData, SupplyChainData, CustomerSatisfactionData, EnergyConsumptionData, MaintenanceData, RDProjectData
import pandas as pd

class Command(BaseCommand):
    help = 'Synchronize dashboard data from Excel files'

    def handle(self, *args, **options):
        tables_path = os.path.join(settings.BASE_DIR, 'tables')
        
        if not os.path.exists(tables_path):
            self.stdout.write(self.style.ERROR(f"Tables directory does not exist: {tables_path}"))
            return

        excel_files = [f for f in os.listdir(tables_path) if f.endswith('.xlsx')]
        
        if not excel_files:
            self.stdout.write(self.style.WARNING("No Excel files found in the tables directory."))
            return

        for file in excel_files:
            file_path = os.path.join(tables_path, file)
            self.process_file(file_path)

        self.stdout.write(self.style.SUCCESS('Dashboard data synchronized successfully'))

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        if re.search(r'sales_data', filename, re.IGNORECASE):
            self.process_sales_data(file_path)
        elif re.search(r'inventory_data', filename, re.IGNORECASE):
            self.process_inventory_data(file_path)
        # Add more conditions for other data types...

    def process_sales_data(self, file_path):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            SalesData.objects.update_or_create(
                date=row['date'],
                product=row['product'],
                defaults={'revenue': row['revenue']}
            )

    def process_inventory_data(self, file_path):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            InventoryData.objects.update_or_create(
                product=row['product'],
                defaults={'quantity': row['quantity'], 'price': row['price']}
            )

    # Add more methods for processing other data types...