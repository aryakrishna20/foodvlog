from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from shop.models import *
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"You Have Been Logged In!")
            return redirect('hm')
        else:
            messages.success(request,"There was an error, please try again.....")
            return redirect('login')
    else:
     return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out.......Thanks for stopping by...")
    return redirect('hm')


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            user.refresh_from_db()  # Refresh user to update the additional fields
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.save()  # Save changes
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)  # Authenticate user
            login(request, user)  # Log in the user
            messages.success(request, "Registration successful!")
            return redirect("hm")  # Redirect to 'hm' or home page
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})