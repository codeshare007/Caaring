import re
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.validators import validate_email

from .models import Cab, User

class NewCabForm(forms.ModelForm):
    #message=forms.CharField(widget=forms.Textarea(), max_length=4000)\

    class Meta:
        model=Cab
        fields = ['name', 'source','destination','dep_date','dep_time','size']

    def clean(self):
        cleaned_data = super(NewCabForm, self).clean()
        try:
            source = self.cleaned_data['source']
            dest = self.cleaned_data['destination']

            if source and dest:
                if source == dest:

                    self.add_error('destination', "Destination cannot be same as Source")
        except:
            pass

class SignupForm(UserCreationForm):

    email=forms.CharField(max_length=50,validators=[
        validators.RegexValidator(re.compile('^[\w.@+-]+$'))
    ])
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','gender','phone_number']


