from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime
from .models import PurchaseHistory

# Create your views here.

def profile(request):
    user = request.user

    return render(request,  'profile.html', {'user':user})

def save_profile_changes(request):
 if request.method == "POST":
   username  = request.POST['username']
   firstname = request.POST['fname']
   lastname = request.POST['lname']
   address = request.POST['address']
   email = request.POST['email']
   phone_number = request.POST['phone_number']
   raw_birthday  = request.POST['bday']

   user = request.user
   try:
        birthday = datetime.strptime(raw_birthday, '%Y-%m-%d').date()
   except ValueError:
        messages.error(request, ("Invalid date format. Please use YYYY-MM-DD."))
        return redirect('profile')

   if user is not None:
     user.username = username
     user.first_name = firstname
     user.last_name = lastname
     user.email = email

     user.userprofile.birthday = birthday
     user.userprofile.address = address
     user.userprofile.phone_number = phone_number

     user.save()

     messages.success(request, ("Profile update successfull!"))
     return redirect('profile')
   else:
    messages.success(request, ("There was an error, please try again..."))
    return redirect('profile')
     
 else:
    return render(request, "profile.html")
 


def history(request):
 user = request.user
 user_purchase_history = PurchaseHistory.objects.filter(user=user)

 return render(request, "history.html", {'user_purchase_history':user_purchase_history})



def security(request):
 return render(request, "security.html")

def save_security_changes(request):
 if request.method == "POST":
        current_pass = request.POST['current_pass']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']

        user = request.user

        if not check_password(current_pass, user.password):
            messages.error(request, "Current password is incorrect.")
            return render(request, "security.html")

        if not new_pass:
            messages.error(request, "Please enter a new password.")
            return render(request, "security.html")

        if new_pass != confirm_pass:
            messages.error(request, "New password and confirm password do not match.")
            return render(request, "security.html")
        
        user.password = make_password(new_pass)
        user.save()

        messages.success(request, "Password updated successfully.")
        return render(request, "security.html")