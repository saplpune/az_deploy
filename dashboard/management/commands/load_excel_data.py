import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import pickle
import re
from dashboard.models import SalesData, InventoryData, Product, Project, Employee, ProductionData, QualityControlData, MachineData, SupplyChainData, CustomerSatisfactionData, EnergyConsumptionData, MaintenanceData, RDProjectData

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load all Excel files from /tables into DataFrames, save as pickle files, and synchronize with database'

    def handle(self, *args, **options):
        tables_dir = os.path.join(settings.BASE_DIR, 'tables')
        pickle_dir = os.path.join(settings.BASE_DIR, 'pickles')
        
        if not os.path.exists(tables_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {tables_dir}"))
            return

        if not os.path.exists(pickle_dir):
            os.makedirs(pickle_dir)

        excel_files = [f for f in os.listdir(tables_dir) if f.endswith('.xlsx')]
        if not excel_files:
            self.stdout.write(self.style.WARNING("No Excel files found in the tables directory."))
            return

        for file in excel_files:
            file_path = os.path.join(tables_dir, file)
            pickle_path = os.path.join(pickle_dir, f"{os.path.splitext(file)[0]}.pkl")
            self.stdout.write(f"Processing file: {file}")
            
            try:
                df = pd.read_excel(file_path)
                print(f"Successfully read {file}")
                print(f"Data sample:\n{df.head()}")
                
                # Save DataFrame as pickle file
                with open(pickle_path, 'wb') as f:
                    pickle.dump(df, f)
                
                self.stdout.write(f"Columns in {file}: {', '.join(df.columns)}")
                self.stdout.write(f"Shape of DataFrame: {df.shape}")
                self.stdout.write(self.style.SUCCESS(f"Successfully loaded {file} into DataFrame and saved as {pickle_path}"))
                
                # Synchronize data with database
                self.sync_data_with_database(file, df)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {file}: {str(e)}"))
                logger.error(f"Error processing {file}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Processed {len(excel_files)} Excel files, saved as pickle files, and synchronized with database"))

    def sync_data_with_database(self, filename, df):
        print(f"Syncing data for {filename}")
        if re.search(r'sales_data', filename, re.IGNORECASE):
            self.sync_sales_data(df)
        elif re.search(r'inventory_data', filename, re.IGNORECASE):
            self.sync_inventory_data(df)
        elif re.search(r'production_data', filename, re.IGNORECASE):
            self.sync_production_data(df)
        # Add more conditions for other data types...

    def sync_sales_data(self, df):
        print(f"Syncing sales data. Rows: {len(df)}")
        for _, row in df.iterrows():
            SalesData.objects.update_or_create(
                date=row['date'],
                product=row['product'],
                defaults={'revenue': row['revenue']}
            )
        self.stdout.write(self.style.SUCCESS("Synchronized sales data"))

    def sync_inventory_data(self, df):
        for _, row in df.iterrows():
            InventoryData.objects.update_or_create(
                product=row['product'],
                defaults={'quantity': row['quantity'], 'price': row['price']}
            )
        self.stdout.write(self.style.SUCCESS("Synchronized inventory data"))

    def sync_production_data(self, df):
        for _, row in df.iterrows():
            ProductionData.objects.update_or_create(
                date=row['date'],
                product=row['product'],
                defaults={'quantity': row['quantity'], 'efficiency': row['efficiency']}
            )
        self.stdout.write(self.style.SUCCESS("Synchronized production data"))

    # Add more methods for synchronizing other data types...