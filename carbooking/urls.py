from django.urls import path
from .import views 
from .views import (
    CarCreateView, 
    CarUpdateView, 
    CarDeleteView,
    ContactCreateView,
) 

urlpatterns = [
    path('', views.home, name='home'),
    path('ContactCreateView/',ContactCreateView.as_view(), name="ContactCreateView"),
    path('CarCreateView/',CarCreateView.as_view(), name="CarCreateView"),
    path('<int:id>/CarUpdateView/',CarUpdateView.as_view(), name="CarUpdateView"),
    path('<int:id>/CarDeleteView/',CarDeleteView.as_view(), name="CarDeleteView"),
    path('cars_detail/', views.cars_detail, name='cars_detail'),
    path('search_results/', views.search_results, name='search_results'),
    path('car_booking/', views.car_booking, name='car_booking'),
    path('user_order_list/', views.user_order_list, name='user_order_list'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<order_id>/', views.order_detail, name='order_detail'),
]