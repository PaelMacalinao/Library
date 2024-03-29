from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def login_user(request):
 if request.method == "POST":
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(request, username=username, password=password)
   if user is not None:
     login(request, user)
     messages.success(request, ("You have been logged In!"))
     return redirect('home')
   else:
    messages.success(request, ("There was an error, please try again..."))
    return redirect('login_user')
     
 else:
    return render(request, "login.html")