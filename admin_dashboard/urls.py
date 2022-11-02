from django.urls import path
from .import views 
 

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('update_order_status/<order_id>', views.update_order_status, name='update_order_status'),
]