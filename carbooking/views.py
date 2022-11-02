import re
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Car, Booking, Contact
from django.contrib.auth.decorators import login_required
from .forms import CarBookingForm, CarCreateForm, ContactForm
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy 
from django.views.generic import CreateView,UpdateView,DeleteView
from datetime import datetime
import pytz
utc=pytz.UTC

# Create your views here.

def home(request):
    return  render(request, 'home.html')

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_message = 'your message Successful send'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

class CarCreateView(SuccessMessageMixin, CreateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'car_create.html'
    success_message = 'Successful Car Added'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CarUpdateView(SuccessMessageMixin, UpdateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'update_car.html'
    success_message = 'Successful Car details Updated'
    success_url = reverse_lazy('home')

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Car, id=id)

class CarDeleteView(SuccessMessageMixin, DeleteView):
    model = Car
    template_name = 'delete_car.html'
    success_message = 'Successful Car deleted'
    success_url = reverse_lazy('cars_detail')

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Car, id=id)

@login_required
def cars_detail(request):
    car = Car.objects.all()

    # pagination
    paginator           = Paginator(car, 3) # Show 3 Cars per page.
    page_number         = request.GET.get('page')
    cars_with_pagination = paginator.get_page(page_number)

    context = {
        'cars_with_pagination': cars_with_pagination
    }
    return render(request, 'booking.html', context)
    

def search_results(request):
    search_input = request.GET.get('search')
    if search_input:
        search_cars = Car.objects.filter(Q(car_name__icontains=search_input) | Q(cost_par_day__icontains=search_input) | Q(car_drive_type__icontains=search_input)).distinct()
    paginator = Paginator(search_cars, 3) # 3 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'search_cars_with_pagination': posts
    }
    return render(request, "search_result.html", context)
    # if 'search' in request.GET and request.GET['search']:
    #     page_number         = request.GET.get('page', 1)
    #     search_input = request.GET.get('search', '')
    #     search_car = Car.objects.filter(Q(car_name__icontains=search_input) | Q(cost_par_day__icontains=search_input) | Q(car_drive_type__icontains=search_input))
    #     paginator           = Paginator(search_car, 3) # Show 3 Cars per page.
        
    #     search_cars_with_pagination = paginator.get_page(page_number)
    #     return render(request, 'search_result.html', context = {'search_cars_with_pagination': search_cars_with_pagination})
    # else:
    #     context = {
    #         'search_cars_with_pagination': search_cars_with_pagination
    #     }
    #     return render(request, 'search_result.html', context)


@login_required
def car_booking(request):
    currentDateTime   = datetime.now()
    currentDate       = currentDateTime.date()

    if request.method == 'POST':
        car_id = request.POST.get('car')
        form = CarBookingForm(request.POST)

        if form.is_valid():
            car_booking                  = form.save(commit=False)
            car_booking.status           = 'In Progress'
            get_all_ids      = list(Booking.objects.filter(car_id=car_id).values_list('id', flat=True))
            get_last_id      = get_all_ids[-1]
            get_data         = Booking.objects.get(pk=get_last_id)
            booking_status   = get_data.status
            car              = get_data.car
            pick_date        = get_data.Pick_up_date_time
            return_date_time = get_data.return_date_time
            return_date      = return_date_time.date()

            if return_date <= currentDate:
                booking_status = get_data.status.replace('In Progress','Completed')
                get_data.status = 'Completed'
                get_data.save()
                print(type(get_data))
                print(f'booking status successfully changed {booking_status}')
            check_car = booking_status in 'In Progress'
            if booking_status  == 'In Progress':
                context = {
                        'pick_date'   : pick_date.date(),
                        'return_date' : return_date,
                        'check_car'   : check_car,
                    }
                return render(request, 'carBooking_message.html', context)
            else:
                if request.user.is_authenticated:
                    car_booking.user = request.user
                car_booking.save()
                context = {
                    'car'  : car,
                }
                return render(request, 'carBooking_message.html', context)

    else:
        form = CarBookingForm()
    context = {
        'form' : form
    }

    return render(request, 'home.html', context)


def user_order_list(request):

    userId = None
    if request.user.is_authenticated:
        userId = request.user.id
    else:
        # Do something for anonymous users.
        pass
    order = Booking.objects.filter(user=userId)
    paginator           = Paginator(order, 5) # Show 3 order per page.
    page_number         = request.GET.get('page')
    order_with_pagination = paginator.get_page(page_number)
    context = {
        'order_with_pagination': order_with_pagination
    }
    return render(request, 'user_order_list.html', context)

def order_list(request):

    order = Booking.objects.all()
    paginator           = Paginator(order, 5) # Show 5 order per page.
    page_number         = request.GET.get('page')
    order_with_pagination = paginator.get_page(page_number)
    context = {
        'order_with_pagination': order_with_pagination
    }
    return render(request, 'order_list.html', context)

def order_detail(request, order_id):

    order_detail = get_object_or_404(Booking,id=order_id)
    context = {
        "order_detail": order_detail,
    }
    return render(request, 'order_detail.html', context)


