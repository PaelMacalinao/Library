from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def register_user(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user_form = UserCreationForm({
            'username': username,
            'email': email,
            'password1': password,
            'password2': password,
        })

        if user_form.is_valid():
            user_form.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have registered successfully.")
            return redirect("home")
        else:
            for error in user_form.errors.values():
                messages.error(request, error.as_text())

    return render(request, "register.html")