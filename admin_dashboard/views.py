from os import remove
from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from carbooking.models import Booking, Car
from django.contrib.auth import get_user_model
from carbooking.forms import CarBookingForm
from django.contrib import messages
# Create your views here.


def admin_home(request):
    order_list = Booking.objects.all()
    
    #Total Clients
    clients = []
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        if request.user.is_superuser == user.is_superuser :
            pass
        else:
    # Where user is whatever foreign key you specified that relates to user.
            clients.append(Booking.objects.filter(user=user))

    total_clients = len(clients)
    
    #Total Revenue
    revenue_list= []
    # order_id = Booking.objects.all().values_list('id', flat=True)
    order = Booking.objects.all().values_list('car__cost_par_day', flat=True)
    for revenue in order:
        revenue_list.append(revenue)
    convert_str_to_int = list(map(int, revenue_list))
    total_revenue = sum(convert_str_to_int)

    #Total Orders
    order = Booking.objects.all()
    total_order = len(order)
    
    #Total Cars
    car = Car.objects.all()
    total_Car = len(car)
    
    #Total Users
    User = get_user_model()
    users = User.objects.all()
    total_user = len(users)

    context = {
        'order_list'    : order_list,
        'total_order'   : total_order,
        'total_Car'     : total_Car,
        'total_clients' : total_clients,
        'total_revenue' : total_revenue,
        'total_user'    : total_user,
    }

    return render(request, 'admin_dashboard.html', context)

def update_order_status(request, order_id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Booking, id = order_id)
 
    # pass the object as instance in form
    form = CarBookingForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to admin_dashboard
    if form.is_valid():
        form.save()
        messages.success(request, ('your status has been successfully updated'))
        return redirect('admin_home')
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "update_order.html", context)