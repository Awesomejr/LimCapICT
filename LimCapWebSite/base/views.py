import os
import requests
import math
import random
from decouple import config

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from typing import Protocol
from django.conf import settings

from .forms import UserRegistrationForm, UserProfileForm, CoursePaymentForm
from .models import Course, User
from .tokens import account_activation_token


# Create your views here.
def index(request):
    return render(request, "./base/homePage.html")


@login_required
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect("base:profilePage", pk=user.id)
    else:
        messages.error(request, 'Activation link is invalid or has expired.')

    return redirect("base:loginPage")  # Redirect to the login page


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("./base/activation_email1.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })

    try:
        validate_email(to_email)
    except ValidationError:
        messages.error(request, "Invalid email address")
        return redirect('base:home')

    email = EmailMessage(mail_subject, message, to=[str(to_email)])
    try:
        email.send()
        messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    except Exception as e:
        messages.error(request, f'Problem sending email to <strong>{to_email}</strong>, check if you typed it correctly.')

    return redirect('base:home')


def registerPage(request):
    courses = Course.objects.all().order_by("name")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            user.username = user.username.lower()
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
            user.course = user.course.title()
            user.save()
            login(request, user)
            print("here")
            messages.success(request,
                             f"New account created: {user.username}. "
                             f"You will receive your activation email shortly or login to activate.")
            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('./base/activation_email1.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            # Getting the pdf file
            with open(os.path.join(settings.BASE_DIR, "static/resources/pdfFiles/manual.pdf"), "rb") as file:
                fileData = file.read()

            email.attach("LimCapICT_Manual.pdf", content=fileData, mimetype="application/pdf")
            email.send()
            # return redirect("base:profilePage", pk=user.id)
            return redirect("base:loginPage")
        else:
            # Form is not valid, display error messages to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()

    context = {"form": form, "courses": courses}
    return render(request, "./base/registrationPage.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("base:home")
    elif request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Does Not Exist!!!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, f"{username.lower()} logged in")
            messages.success(request, f"{user.username} is now logged in.")
            return redirect("base:profilePage", pk=user.id)
        else:
            messages.error(request, "Incorrect Username or Password!!!")

    return render(request, "./base/loginPage.html")


# @login_required(login_url="/login")
def profilePage(request, pk):
    user = get_object_or_404(User, id=pk)
    course = Course.objects.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=True)
            user.username = user.username.lower()
            user.first_name = user.first_name.capitalize()
            user.last_name = user.last_name.capitalize()
            user.gender = user.gender.capitalize()
            user.course = user.course.capitalize()
            user.save()
            messages.success(request, "Profile Updated!!!")
            # return redirect('base:profilePage')  # Redirect to the user's profile page
    else:
        form = UserProfileForm(instance=user)  # Pass the user instance here

    context = {"courses": course, "form": form, "user": user}
    return render(request, './base/profilePage.html', context=context)

def purchaseCourse(request, pk):
    user = User.objects.get(id=pk)
    course = Course.objects.get(id=pk)

    # Prefill form with user details and course information
    initialData = {
        "userId": user.id,
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "phoneNumber": user.phoneNumber,
        "description": course.description,
        "amount": course.price,
    }
    form = CoursePaymentForm(initial=initialData)

    if request.method == "POST":
        form = CoursePaymentForm(request.POST)
        if form.is_valid():
            # Retrieve cleaned data from the form
            cleaned_data = form.cleaned_data
            userId = user.id
            username = user.username
            firstName = cleaned_data["firstName"]
            lastName = cleaned_data["lastName"]
            email = cleaned_data["email"]
            phoneNumber = cleaned_data["phoneNumber"]
            description = cleaned_data["description"]
            amount = cleaned_data["amount"]
            
            # Process the payment and redirect to a success page
            processPayment(userId, username, firstName, lastName, email, phoneNumber, course, description, amount)
            return redirect('payment_success')  # Redirect to a URL or view name
            
    context = {"courseToPurchase": course, "form": form}
    return render(request, './base/coursePaymentPage.html', context=context)

def processPayment(userId, username, firstName, lastName, email, phoneNumber, course, description, amount):
     auth_token= config('SECRET_KEY')
     hed = {'Authorization': 'Bearer ' + auth_token}
     data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"NGN",
                "redirect_url":"https://127.0.0.1:8000/confirmPayment/" + userId,
                "payment_options":"card",
                "meta":{
                    "consumer_id":userId,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":email,
                    "phonenumber":phoneNumber,
                    "name": f"{firstName} {lastName} @{username}"
                },
                "customizations":{
                    "title":"LimCapICT BootCamp",
                    "description": description,
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
     url = ' https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     link=response['data']['link']
     return link

@require_http_methods(['GET', 'POST'])
def confirmPayment(request):
    status = request.GET.get("status", None)
    tex_ref = request.GET.get("tx_ref", None)

    user = User.objects.get(pk=id)
    user.paymentStatus = "Paid"
    user.save()
    messages = f"{status}!!! \nCongratulation {user.first_name} {user.last_name}! Your payment was successful."
    messages.success(request, messages)
    return redirect("base:profilePage", pk=user.id)


def aboutPage(request):
    return render(request, "./base/aboutPage.html")


def logoutUser(request):
    logout(request)
    return redirect("base:home")
