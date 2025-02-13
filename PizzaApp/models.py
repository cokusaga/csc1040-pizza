from django.db import models
from django.contrib.auth.models import User

# Pizza Size Model
class PizzaSize(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10.99)  # Default price

    def __str__(self):
        return self.name

# Pizza Crust Model
class PizzaCrust(models.Model):
    name = models.CharField(max_length=100, default="Normal")  # Default crust

    def __str__(self):
        return self.name

# Pizza Sauce Model
class PizzaSauce(models.Model):
    name = models.CharField(max_length=100, default="Tomato")  # Default sauce

    def __str__(self):
        return self.name

# Pizza Cheese Model
class PizzaCheese(models.Model):
    name = models.CharField(max_length=100, default="Mozzarella")  # Default cheese

    def __str__(self):
        return self.name

# Pizza Topping Model
class PizzaTopping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='toppings_images/', null=True, blank=True)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pizza_size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE, default=1)  # Default size ID
    pizza_crust = models.ForeignKey(PizzaCrust, on_delete=models.CASCADE, default=1)  # Default crust ID
    pizza_sauce = models.ForeignKey(PizzaSauce, on_delete=models.CASCADE, default=1)  # Default sauce ID
    pizza_cheese = models.ForeignKey(PizzaCheese, on_delete=models.CASCADE, default=1)  # Default cheese ID
    toppings = models.ManyToManyField(PizzaTopping, blank=True)

    # Payment & Delivery Fields with Defaults
    full_name = models.CharField(max_length=100)
    delivery_address = models.TextField()
    card_number = models.CharField(max_length=16, default="0000000000000000")  # Fake card for DB
    card_expiry_date = models.CharField(max_length=5, default="00/00")  # Placeholder
    card_cvv = models.CharField(max_length=3, default="000")  # Placeholder

    def total_price(self):
        """
        Calculate total price including pizza size and toppings.
        """
        base_price = self.pizza_size.price if self.pizza_size else 0
        toppings_price = sum(t.price for t in self.toppings.all())
        
        return base_price + toppings_price

    def __str__(self):
        return f"Order {self.id} - {self.pizza_size.name if self.pizza_size else 'Unknown'}"