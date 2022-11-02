from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from datetime import datetime 

# Create your models here.

choices = (('Completed', 'Completed'),
        ('cancled', 'cancled'), 
        ('In Progress','In Progress'),
        )

class Car(models.Model):
    author   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    car_name = models.CharField(max_length=100)
    car_drive_type = models.CharField(max_length=30)
    num_of_seats = models.IntegerField()
    num_of_luggages = models.IntegerField()
    num_of_doors = models.IntegerField()
    cost_par_day = models.CharField(max_length=50)
    content = models.TextField()
    isBooked = models.BooleanField(default=False)

    def __str__(self):
        return self.car_name

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/images/user.jpg"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    pick_up_location = models.CharField(max_length=200)
    return_location = models.CharField(max_length=200)
    Pick_up_date_time = models.DateTimeField(default=datetime.now, blank=True)
    return_date_time = models.DateTimeField()
    full_name = models.CharField(max_length=50)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    email_address = models.EmailField()
    phone = models.IntegerField()
    status = models.CharField(max_length = 100, choices = choices, default="In Progress")

    def __str__(self):
        return str(self.user)
    
class Contact(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email_address = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return str(self.client)
    