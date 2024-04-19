from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.




class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)
    middle_name = models.CharField(max_length=64, blank=False, null=False)
    phone_number = models.CharField(max_length=64, blank=True)
    address1 = models.CharField(max_length=64, blank=True)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    budget = models.IntegerField(default=100000)
    
    def __str__(self):
        return'{} {}'.format(self.first_name, self.last_name)
    
    def valid_user(self):
        if (self.first_name and self.last_name and self.email and 
            self.phone_number and self.address1 and self.city and self.state and self.password):
            return True
        else:
            return False


    def can_purchase(self, total):
        # checking if the user has enough budget
        return self.budget >= total
    
    

class Product(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    price = models.IntegerField()
    description = models.CharField(max_length=124)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True) 
    product_timestamp = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='selling_products')
    img = models.ImageField(default='foodnet/assets/default.jpg', upload_to='images') 

    def __str__(self):
        return f"{(self.name).title()}"
    
    def valid_product(self):
        if self.name and self.price > 0 and self.category and self.vendor.valid_user():
            return True
        else:
            return False



class Order(models.Model):
    client = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=64, default='shopping')
    transaction_id = models.CharField(max_length=64)

    def __str__(self):
        return f"Order {self.id}"
    
    def valid_order(self):
        if self.client.valid_user() and self.transaction_id:
            return True
        else:
            return False
    
    # to get the total amount of an order
    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total_amount = sum([item.get_total for item in orderitems])

        return total_amount

    # to get the total quantity of an order
    @property
    def get_cart_items(self):
        # orderitems = self.orderitem_set.all() (if a related_name was not given)
        orderitems = self.order_items.all()
        total_quantity = sum([item.quantity for item in orderitems])

        return total_quantity

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, related_name='order_products', null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, related_name='order_items', null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order Item {self.id}"
    
    # get the total amount of the quantity of an order item
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

    def valid_orderItem(self):
        if (self.product.valid_product() and self.order.valid_order() and 
            self.quantity > 1 and self.product.vendor != self.order.client):
            return True
        else:
            return False

class ShippingAddress(models.Model):
    client = models.ForeignKey('User', on_delete=models.SET_NULL,  related_name='user_shipping', null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, related_name='order_shipping', null=True)
    name = models.CharField(max_length=200)
    phone_number =models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Shipping {self.id}"

    def valid_shipping(self):
        if (self.client.valid_user() and self.order.valid_order() and
             self.name and self.phone_number and self.address and self.client == self.order.client and
             self.city and self.state):
            return True
        else:
            return False

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{(self.category).title()}"