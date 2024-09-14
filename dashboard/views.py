import logging
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SalesData, InventoryData, Product, Project, Employee, ProductionData, QualityControlData, MachineData, SupplyChainData, CustomerSatisfactionData, EnergyConsumptionData, MaintenanceData, RDProjectData
from django.db.models import Sum, Count, F, Avg
from django.core.cache import cache

logger = logging.getLogger(__name__)

# Cache key for our data
DATA_CACHE_KEY = 'dashboard_data'
# How often to refresh the data (in seconds)
REFRESH_INTERVAL = 3600  # 1 hour

def dashboard(request):
    context = get_dashboard_data()
    
    # Add debug information
    debug_info = {
        "Project Count": Project.objects.count(),
        "Sales Data Count": SalesData.objects.count(),
        "Inventory Data Count": InventoryData.objects.count(),
        "Production Data Count": ProductionData.objects.count(),
        "Employee Count": Employee.objects.count(),
    }
    context['debug_info'] = debug_info
    
    return render(request, 'dashboard/index.html', context)

def get_dashboard_data():
    cached_data = cache.get(DATA_CACHE_KEY)
    if cached_data is None:
        data = process_data()
        if data:
            cache.set(DATA_CACHE_KEY, data, REFRESH_INTERVAL)
        return data
    return cached_data

def process_data():
    context = {}
    try:
        context['total_products'] = Product.objects.count()
        context['low_stock_items'] = InventoryData.objects.filter(quantity__lt=10).count()
        context['total_inventory_value'] = InventoryData.objects.aggregate(total_value=Sum(F('quantity') * F('price')))['total_value'] or 0
        context['total_sales'] = SalesData.objects.filter(date__gte=timezone.now() - timedelta(days=30)).aggregate(Sum('revenue'))['revenue__sum'] or 0
        
        context['top_products'] = list(SalesData.objects.values('product__name').annotate(total_sales=Sum('revenue')).order_by('-total_sales')[:5])
        
        context['active_projects'] = Project.objects.filter(status='in_progress').count()
        context['completed_projects'] = Project.objects.filter(status='completed').count()
        context['upcoming_projects'] = Project.objects.filter(status='planning').count()
        
        context['total_employees'] = Employee.objects.count()
        context['departments'] = list(Employee.objects.values('department').annotate(count=Count('id')))
        
        context['avg_production_efficiency'] = ProductionData.objects.aggregate(Avg('efficiency'))['efficiency__avg'] or 0
        context['total_production_output'] = ProductionData.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        context['quality_control'] = QualityControlData.objects.aggregate(total_defects=Sum('defects'))['total_defects'] or 0
        context['machine_uptime'] = MachineData.objects.aggregate(avg_uptime=Avg('uptime'))['avg_uptime'] or 0
        context['avg_lead_time'] = SupplyChainData.objects.aggregate(Avg('lead_time'))['lead_time__avg'] or 0
        context['customer_satisfaction'] = CustomerSatisfactionData.objects.aggregate(Avg('satisfaction_score'))['satisfaction_score__avg'] or 0
        context['energy_consumption'] = EnergyConsumptionData.objects.aggregate(total_consumption=Sum('consumption'))['total_consumption'] or 0
        context['maintenance_hours'] = MaintenanceData.objects.aggregate(total_duration=Sum('duration'))['total_duration'] or 0
        context['rd_projects'] = RDProjectData.objects.count()
        context['rd_budget'] = RDProjectData.objects.aggregate(total_budget=Sum('budget'))['total_budget'] or 0

        logger.debug(f"Processed data: {context}")
    except Exception as e:
        logger.exception(f"Error processing data: {str(e)}")
        context['error'] = f"Error processing data: {str(e)}"
    return context
