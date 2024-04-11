from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Order, OrderItem, Product, Category, ShippingAddress
from .forms import RegisterForm, LoginForm
from django.shortcuts import redirect
from django.contrib import messages
from .templatetags.my_filter import naira
from django.utils import timezone
from django.contrib import messages


# Create your views here.

def home_page(request):
    return render(request, "foodnet/home_page.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:

            messages.info(request, 'Invalid username and/or password.')
            return render(request, "foodnet/login.html")
    else:
        return render(request, "foodnet/login.html", {
            "form": LoginForm()
        })
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))



def register(request):
    if request.method == "POST":
        
        first_name = request.POST.get("first_name", False)
        surname = request.POST.get("surname", False)
        middle_name = request.POST.get("middle_name", False)
        username = request.POST["username"]
        email = request.POST.get("email", False)
        
        password = request.POST.get("password", False)
        confirmation = request.POST.get("confirm_password", False)
        
        phone_number = request.POST.get("phone_number", False)
        address1 = request.POST.get("address1", False)
        address2 = request.POST.get("address2", False)        
        state = request.POST.get("state", False)
        city = request.POST.get("city", False)
        zipcode = request.POST.get("zip", False)


        if not(first_name) or not(surname) or not(username) or not(phone_number) or \
            not(address1) or not(city) or not(state):

            messages.warning(request, 'Please fill the form correctly.')
            return render(request, "foodnet/register.html")

        # Ensure password matches confirmation
        if password != confirmation:

            messages.warning(request, 'Passwords must match.')
            return render(request, "foodnet/register.html")

        # Attempt to create new user
        try:
            if not(address2):
                user = User.objects.create_user(first_name=first_name, last_name=surname, middle_name = middle_name, username=username
                                                , email=email, password=password, phone_number=phone_number, address1=address1)
            else:
                user = User.objects.create_user(first_name=first_name, last_name=surname, middle_name = middle_name, username=username
                                                , email=email, password=password, phone_number=phone_number, address1=address1, address2=address2
                                                , state=state, city=city, zipcode=zipcode)

            user.save()
        except IntegrityError:

            messages.info(request, 'Username already taken.')
            return render(request, "foodnet/register.html")
        
        login(request, user)

        messages.success(request, 'Welcome the FoodNet community !! Your account has been created.')
        return HttpResponseRedirect(reverse("market"))
    else:
        return render(request, "foodnet/register.html", {
            "form": RegisterForm(),
        })


def market(request):

    products = Product.objects.all().order_by('product_timestamp')

    return render(request, "foodnet/market.html", {
        'products': products,
    })


@login_required(login_url="/login")
def cart(request):
    return render(request, "foodnet/cart.html")


@login_required(login_url="/login")
def checkout(request):
    return render(request, "foodnet/checkout.html")


def view_product(request):
    return render(request, "foodnet/view_product.html")


@login_required(login_url="/login")
def create_product(request):
    return render(request, "foodnet/create_product.html")


@login_required(login_url="/login")
def profile(request):
    return render(request, "foodnet/profile.html")
