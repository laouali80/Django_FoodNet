from django.contrib import admin
from .models import User, Order, OrderItem, Product, Category, ShippingAddress
# Register your models here.

# configuration of admin for getting more information
# class FlightAdmin(admin.ModelAdmin):
#     list_display = ("id","origin","destination","duration")

# # Special way of managing many to many relationship
# class PassengerAdmin(admin.ModelAdmin):
#     filter_horizontal = ("flights",)
    
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(ShippingAddress)
# admin.site.register(Flight, FlightAdmin)
# admin.site.register(Passenger, PassengerAdmin)
# admin.site.register(Event)