# views.py
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='http:127.0.0.1:8000/login')
def homepage(request):
    return render(request=request, template_name='main/home.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            
            # Check if passwords match
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request=request, template_name="main/register.html", context={"register_form": form})
            
            # Check if username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return render(request=request, template_name="main/register.html", context={"register_form": form})
            
            # Check if email is already taken
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email is already taken.")
                return render(request=request, template_name="main/register.html", context={"register_form": form})
            
            # If everything is fine, proceed with registration
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("http://localhost:8000/login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("http://127.0.0.1:8000")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("http://127.0.0.1:8000/login")

@login_required(login_url='http://127.0.0.1:8000/login')
def profile_section(request):
    return render(request=request, template_name="main/profile_section.html")
