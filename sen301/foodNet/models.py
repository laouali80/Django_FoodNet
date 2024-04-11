from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.




class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    middle_name = models.CharField(max_length=64, blank=False, null=False)
    email = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=64, blank=True)
    address1 = models.CharField(max_length=64, blank=True)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    budget = models.IntegerField(default=10000)
    # cart = models.ManyToManyField("Product", related_name="carts")
    # orders = models.ManyToManyField("Order", related_name="orders")
    
    def __str__(self):
        return'{} {}'.format(self.first_name, self.last_name)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'₦{str(self.budget)[:-3]},{str(self.budget)[-3:]}.00'
        else:
            return f'₦{str(self.budget)}.00'

    def can_purchase(self, item):
        # checking if the user has enough budget
        return self.budget >= item.price
    
    def can_sell(self, item):
        # checking if the user has the item
        return item in self.items

class Product(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    price = models.IntegerField()
    description = models.CharField(max_length=124)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True) 
    product_timestamp = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='seller')
    img = models.ImageField(default='foodnet/assets/default.jpg', upload_to='images') 

    def __repr__(self):
        return f"{(self.name).title()}"

#     def buy(self, user):

#         # assign to the current user the item
#         self.owner = user.id
#         self.possesion = user.id
#         # debitting the user account
#         user.budget -= self.price

#         db.session.commit()

#     def sell(self, user):
#         # depossess the current user the item
#         self.possesion = None

#         # crediting the user account
#         user.budget += self.price

#         db.session.commit()


class Order(models.Model):
    vendor = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='customer', null=True, blank=True)
    client = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='client', null=True, blank=True)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=64)
    # transtion_id = models.CharField(max_length=64)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_timestamp = models.DateTimeField(auto_now_add=True)
    # vendor = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='customer', null=True, blank=True)
    # client = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='client', null=True, blank=True)
    
    def __str__(self):
        return f"Order Item {self.id}"
    

class ShippingAddress(models.Model):
    vendor = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='sender', null=True, blank=True)
    client = models.ForeignKey('User', on_delete=models.SET_NULL,  related_name='receiver',null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Shipping {self.id}"


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{(self.category).title()}"