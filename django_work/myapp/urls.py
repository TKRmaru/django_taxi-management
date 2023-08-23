from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import get_car_mileage

app_name = 'myapp'
urlpatterns = [
    path('', login_required(views.Home.as_view()), name='home'),
    path('car_create/', login_required(views.CarCreateView.as_view()), name='car_create'),
    path('car_list/', login_required(views.CarListView.as_view()), name='car_list'),
    path('car_update/<int:pk>', login_required(views.CarUpdateView.as_view()), name='car_update'),
    path('car_delete/<int:pk>', login_required(views.CarDeleteView.as_view()), name='car_delete'),
    path('customer_create/', login_required(views.CustomerCreateView.as_view()), name='customer_create'),
    path('customer_list/', login_required(views.CustomerListView.as_view()), name='customer_list'),
    path('customer_detail/<int:pk>', login_required(views.CustomerDetailView.as_view()), name='customer_detail'),
    path('customer_update/<int:pk>', login_required(views.CustomerUpdateView.as_view()), name='customer_update'),
    path('customer_delete/<int:pk>', login_required(views.CustomerDeleteView.as_view()), name='customer_delete'),
    path('place_create/', login_required(views.PlaceCreateView.as_view()), name='place_create'),
    path('place_list/', login_required(views.PlaceListView.as_view()), name='place_list'),
    path('place_detail/<int:pk>', login_required(views.PlaceDetailView.as_view()), name='place_detail'),
    path('place_update/<int:pk>', login_required(views.PlaceUpdateView.as_view()), name='place_update'),
    path('place_delete/<int:pk>', login_required(views.PlaceDeleteView.as_view()), name='place_delete'),
    path('data_input/', login_required(views.DataInputView.as_view()), name='data_input'),
    path('myapp/get_car_mileage/<int:car_id>/', get_car_mileage, name='get_car_mileage'),
    path('data_list/', login_required(views.DataListView.as_view()), name='data_list'),
    path('data_summary/', login_required(views.DataSummaryView.as_view()), name='data_summary'),
    path('data_detail/<int:pk>', login_required(views.DataDetailView.as_view()), name='data_detail'),
    path('data_update/<int:pk>', login_required(views.DataUpdateView.as_view()), name='data_update'),
    path('data_delete/<int:pk>', login_required(views.DataDeleteView.as_view()), name='data_delete'),
    path('car/csv_export/', login_required(views.CarCSVExportView.as_view()), name='car_csv_export'),
    path('car/csv_import/', login_required(views.CarCSVImportView.as_view()), name='car_csv_import'),
    path('customer/csv_export/', login_required(views.CustomerCSVExportView.as_view()), name='customer_csv_export'),
    path('customer/csv_import/', login_required(views.CustomerCSVImportView.as_view()), name='customer_csv_import'),
    path('place/csv_export/', login_required(views.PlaceCSVExportView.as_view()), name='place_csv_export'),
    path('place/csv_import/', login_required(views.PlaceCSVImportView.as_view()), name='place_csv_import'),
    path('data_list/csv_export/', login_required(views.DataListCSVExportView.as_view()), name='data_list_csv_export'),
    path('data_list/csv_import/', login_required(views.DataCSVImportView.as_view()), name='data_list_csv_import'),
    path('data_summary/csv_export/', login_required(views.DataSummaryCSVExportView.as_view()), name='data_summary_csv_export'),
]
