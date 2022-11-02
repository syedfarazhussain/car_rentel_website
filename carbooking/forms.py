from django.forms import ModelForm
from .models import Booking, Car, Contact


class CarBookingForm(ModelForm):
    class Meta:
        model = Booking
        fields =  ['pick_up_location', 'return_location', 'Pick_up_date_time','car', 'return_date_time','full_name','email_address','phone','status',]

    def __init__(self, *args, **kwargs):
        super(CarBookingForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 'In Progress'
        self.fields['status'].required = False


class CarCreateForm(ModelForm):
    class Meta:
        model = Car
        fields =  ['image', 'car_name', 'car_drive_type','num_of_seats', 'num_of_luggages','num_of_doors','cost_par_day','content',]

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields =  ['name', 'email_address', 'subject','message',]
        