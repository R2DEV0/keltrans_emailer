from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import os
import smtplib
from email.message import EmailMessage


# first page of app, login/registration #
def index(request):
    return render(request, 'login.html')


# login existing user created by Admin #
def login(request):
    errors = User.objects.return_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    login_user_list = User.objects.filter(email=request.POST['email'])  
    logged_in_user = login_user_list[0]
    request.session['user_id'] = logged_in_user.id
    return redirect('/dashboard')


# logs in a new user if validations pass #
def new_user(request):
    errors = User.objects.new_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name= request.POST['name']
        email= request.POST['email']
        password= request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(name=name, home=home, email=email, password=pw_hash)
        request.session['user_id'] = new_user.id
    return redirect('/dashboard')


# main dashboard page #
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'dashboard.html', context)


# Email blaster function #
def blast(request):
# set email and password variables from form #
    email_address = request.POST['email']
    email_password = request.POST['password']

# set contact list to be email blasted from form #
    form_contacts = request.POST['email_to']
    contacts = form_contacts.split()

# set subject and message variables from form #
    email_subject = request.POST['subject']
    email_message = request.POST['message']

# run a for loop to email each contact directly #
    for contact in contacts:
        msg = EmailMessage()
        msg['Subject'] = email_subject
        msg['From'] = email_address
        msg['To'] = contact
        msg.set_content(email_message)

# login to my email and send! #
        with smtplib.SMTP_SSL('secure.emailsrvr.com', 465) as smtp:
            try:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
            except Exception:
                error = {
                    'error': 'Your password is not correct'
                }
                return render(request, 'dashboard.html', error)
    return redirect('/dashboard')


# Logout user and return to login page #
def logout(request):
    request.session.flush()
    return redirect('/')
