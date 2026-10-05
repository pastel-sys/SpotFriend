from django.contrib.auth import authenticate, login, logout

import os
import hashlib
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.urls import reverse
from .models import User
from datetime import datetime

# Keys to interact with the Lastfm API
load_dotenv()
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
SHARED_SECRET = os.getenv('SHARED_SECRET')

# Default Page of the app
def index(request):
    # Redirect the user to his dashboard 
    lastfm_session = ""
    if not request.user.is_anonymous:
        user_key = User.objects.get(id=request.user.id)
        lastfm_session = user_key.has_session
        if lastfm_session == True:
            return redirect("http://127.0.0.1:8000/dashboard")
    
    try:
        # requesting a session for the user
        TOKEN = request.GET["token"]
        sign_str = f"api_key{LASTFM_API_KEY}methodauth.getSessiontoken{TOKEN}{SHARED_SECRET}"
        api_sig = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
        session_params = {
            "method": "auth.getSession",
            "api_key": LASTFM_API_KEY,
            "token": TOKEN,
            "api_sig": api_sig,
            "format": "json", 
        }
        session = requests.get("https://ws.audioscrobbler.com/2.0/", params=session_params)

        # saving the session response in the database
        user = User.objects.get(id=request.user.id)
        user.lastfm_username = session.json()["session"]["name"]
        user.lastfm_session_key = session.json()["session"]["key"]
        user.save()
        return redirect("http://127.0.0.1:8000/dashboard")
    except:
        None

    return render(request, "spot/index.html", {
        "is_authenticated": request.user.is_authenticated,
    })

# Redirect to synchronizate with Lastfm
def synch_lastfm(request):
    return redirect(f"http://www.last.fm/api/auth/?api_key={LASTFM_API_KEY}&cb=http://127.0.0.1:8000/dashboard")

# Default page view for a logged and synchronized user
def dashboard(request):
    # ensure the user has synchronized the app with his lastfm account
    if request.user.has_session == False:
        return redirect("http://127.0.0.1:8000/")

    user = request.user
    
    
    return render(request, "spot/dashboard.html", {
        "is_authenticated": request.user.is_authenticated,
        "user": user
    })

# Login function 
def login_user(request):
    if request.method == "POST": 
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        # ensure is a valid user
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            return render(request, "spot/login.html", {
                "loginMsg": "Something is Wrong. Check your username or password.",
            })
    else:
        return render(request, "spot/login.html")

# Logout function
def logout_user(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

# Register function
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