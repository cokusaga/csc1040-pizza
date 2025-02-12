from django.contrib import admin
from .models import PizzaSize, PizzaCrust, PizzaSauce, PizzaCheese, PizzaTopping, Order

# Register models in the admin interface
admin.site.register(PizzaSize)
admin.site.register(PizzaCrust)
admin.site.register(PizzaSauce)
admin.site.register(PizzaCheese)
admin.site.register(PizzaTopping)
admin.site.register(Order)
