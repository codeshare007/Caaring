from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
APPROVED='Approved'
DECLINED='Declined'
REQUESTED='Requested'

class User(AbstractUser):
    GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female')
    )
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be of 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=False)




class Cab(models.Model):
    PLACE_CHOICES=(
        ('VIT','VIT VELLORE'),
        ('Bangalore','BANGALORE'),
        ('Chennai','CHENNAI'),
        ('Hyderabad','HYDERABAD')
    )
    name_regex=RegexValidator(regex=r'^[-.@+\w]+$',message="Field can contain only a-z , A-Z , 0-9 , _ , . , @ , - , + ",code='invalid name')
    name=models.CharField(max_length=25,unique=True,validators=[name_regex])
    source=models.CharField(max_length=10,choices=PLACE_CHOICES)
    destination=models.CharField(max_length=10,choices=PLACE_CHOICES)
    dep_date=models.DateField(help_text='Input in format "YYYY-mm-dd"')
    dep_time=models.TimeField(help_text='Input in format "HH:MM"')
    size=models.IntegerField(validators=[MaxValueValidator(7), MinValueValidator(3)])
    seats_left=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    cab_admin=models.ForeignKey(User,related_name="cab_admin",on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.name)


class Passenger(models.Model):
    STATUS_CHOICES=(
        (APPROVED,'APPROVED'),
        (DECLINED,'DECLINED'),
        (REQUESTED,'REQUESTED')
    )
    is_admin=models.BooleanField(default=False)
    approval_status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user")
    of_cab=models.ForeignKey(Cab,related_name="of_cab")

    def __str__(self):
        return str(self.user.username)
