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
    if request.user.is_authenticated:
        return redirect('market')
    return render(request, "foodnet/home_page.html")


def login_view(request):

    # redirect the user to market if he is login
    if request.user.is_authenticated:
        return redirect('market')
    
    if request.method == "POST":

        # recuperation of the data first
        form = LoginForm(request.POST)

        if form.is_valid():
            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(type(username))
            print(type(password))
            user = authenticate(request, username=username, password=password)

            print(authenticate(request, username=username, password=password))
            
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("market"))
            else:
                    
                messages.info(request, 'Invalid Username/Password! Please Try again.')
                return render(request, "foodnet/login.html", {
                "form": form
            })
                
        else:

            messages.warning(request, 'Please fill the form to login!!')
            return render(request, "foodnet/login.html", {
            "form": form
        })
    else:
        return render(request, "foodnet/login.html", {
            "form": LoginForm()
        })
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):

    #  redirect the user if he is login
    if request.user.is_authenticated:
        return redirect('market')
    
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


@login_required(login_url="/foodNet/login/")
def cart(request):
    return render(request, "foodnet/cart.html")


@login_required(login_url="foodNet/login")
def checkout(request):
    return render(request, "foodnet/checkout.html")


def view_product(request, product_id):

    try:  
        product = Product.objects.get(pk=int(product_id))
    except UnboundLocalError or ValueError:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('market')
    except Product.DoesNotExist:
        messages.info(request, '404 Not Found!! Product not found.')
        return redirect('market')
    
    return render(request, "foodnet/view_product.html",{
        'product':product,
    })


@login_required(login_url="/foodNet/login/")
def create_product(request):
    if request.method == "POST":
        
        name = request.POST.get("name", False)
        description = request.POST.get("description", False)
        price = request.POST.get("price", False)
        category = request.POST.get("category", False)
        image = request.FILES.get("image", False)

        # print(image)
        
        if not(name) or not price.isdigit() or not category:
            messages.warning(request, 'Please fill the form correctly.')
            return render(request, "foodnet/create_product.html")
        
        try:
            # if the user provides the image
            if image:
                try:
                    if Category.objects.get(pk=int(category)):
                        product = Product.objects.create(name=name, description=description, price=price,
                                                        img=image, vendor=request.user, category=Category.objects.get(pk=int(category)))
                        product.save()
                except IntegrityError and ValueError:

                    messages.info(request, 'Sorry something went wrong!! Please try again.')
                    return render(request, "auctions/create_listing.html")
                
            # if the user does not provide the image
            else:
                try:
                    if Category.objects.get(pk=int(category)):
                        product = Product.objects.create(name=name, description=description, price=price,
                                                        vendor=request.user, category=Category.objects.get(pk=int(category)))
                        product.save()
                except IntegrityError and ValueError:

                    messages.info(request, 'Sorry something went wrong!! Please try again.')
                    return render(request, "auctions/create_listing.html")

        except IntegrityError or KeyError:

            messages.info(request, 'Sorry something went wrong!! Please try again.')
            return render(request, "auctions/create_listing.html")

        
        messages.success(request, f'Your product {name.title()} has been added to the market for {naira(int(price))}.')
        return HttpResponseRedirect(reverse("market"))

    else:
        categories = Category.objects.all()

        return render(request, "foodnet/create_product.html", {
            'categories': categories
        })


@login_required(login_url="/foodNet/login/")
def profile(request, prof_name, prof_id):
    try:  
        profile = User.objects.get(pk=int(prof_id))

        if profile.username != prof_name:
            return redirect('market')
        
    except UnboundLocalError or ValueError:
        return redirect('market')
    except Product.DoesNotExist:
        return redirect('market')
    
    return render(request, "foodnet/profile.html", {
        'profile': profile,
    })
