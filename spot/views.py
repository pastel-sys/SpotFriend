from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from datetime import datetime

def index(request):
    return render(request, "spot/index.html", {
        "is_authenticated": request.user.is_authenticated
    })

def login_user(request):
    if request.method == "POST": 
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            return render(request, "spot/login.html", {
                "loginMsg": "Something is Wrong. Check your username or password.",
            })
    else:
        return render(request, "spot/login.html")

def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #ensure that passwords matches
        password = request.POST["password"]
        if password != request.POST["repeatedPassword"]:
            return render(request, "spot/register.html", {
                "registerMsg": "Passwords must match",
            })

        newuser = User.objects.create_user(username=username, email=email, password=password, first_name=request.POST["name"], last_name=request.POST["lastname"], birthdate=request.POST["birthdate"])
        login(request, newuser)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "spot/register.html")