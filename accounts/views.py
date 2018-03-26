from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

# Create your views here.
from caaring.forms import SignupForm


def Signup(request):
    if request.method == 'POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save(commit=True)
            auth_login(request,user)
            return redirect('home')

    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})
