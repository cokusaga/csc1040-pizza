from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import PizzaOrderForm, DeliveryDetailsForm

# Home page view
def index(request):
    return render(request, 'index.html')

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after successful login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Dashboard view - lists orders of the logged-in user
@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)  # Get orders for logged-in user
    return render(request, 'dashboard.html', {'orders': orders})

# Create pizza view - allows a user to create a new pizza order
@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = PizzaOrderForm(request.POST)
        if form.is_valid():
            pizza_order = form.save(commit=False)  
            pizza_order.user = request.user  
            pizza_order.save()  

            form.save_m2m()  # Save many-to-many toppings

            # Debugging output to check what's happening
            print(f"Order created with ID: {pizza_order.id}")  # This checks that the order is being created correctly

            # Attempting to redirect to the payment page
            try:
                redirect_url = redirect('payment', order_id=pizza_order.id)
                print(f"Redirecting to: {redirect_url}")  # This checks the redirect URL
                return redirect_url
            except Exception as e:
                print(f"Error during redirection: {e}")  # If there's an error during redirection
        else:
            print(f"Form errors: {form.errors}")  # Print form errors if form is invalid

    else:
        form = PizzaOrderForm()

    return render(request, 'create_pizza.html', {'form': form})

# Payment view - allows user to enter payment and delivery details
@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        form = DeliveryDetailsForm(request.POST, instance=order)
        if form.is_valid():
            # Save form details to the existing order
            order.full_name = form.cleaned_data['full_name']
            order.delivery_address = form.cleaned_data['delivery_address']

            # Only store the last 4 digits of the card number for security
            card_number = form.cleaned_data['card_number']
            order.card_number = f"**** **** **** {card_number[-4:]}"  

            order.card_expiry_date = form.cleaned_data['card_expiry_date']
            # Avoid storing CVV (PCI compliance)
            # order.card_cvv = form.cleaned_data['card_cvv']

            order.save()  # Save the updated order with delivery details

            print(f"Order ID: {order.id}")  # Debugging

            messages.success(request, "Payment details saved successfully!")
            return redirect('order_confirmation', order_id=order.id)
        else:
            print("Form is invalid. Errors:", form.errors)  # Debugging
            messages.error(request, "Invalid form submission. Please check your details.")
    else:
        # Pre-fill form with existing order details (if available)
        form = DeliveryDetailsForm(instance=order)

    return render(request, 'payment.html', {'form': form, 'order': order})

# Order confirmation view - shows details of the placed order
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get the pizza size, crust, sauce, cheese, and toppings
    pizza_size = order.pizza_size.name if order.pizza_size else "No size selected"
    pizza_crust = order.pizza_crust.name if order.pizza_crust else "No crust selected"
    pizza_sauce = order.pizza_sauce.name if order.pizza_sauce else "No sauce selected"
    pizza_cheese = order.pizza_cheese.name if order.pizza_cheese else "No cheese selected"
    toppings = order.toppings.all()

    # Only show the last 4 digits of the card number for security
    last_four_digits = order.card_number[-4:] if order.card_number and len(order.card_number) >= 4 else "****"

    return render(request, 'order_confirmation.html', {
        'order': order,
        'pizza_size': pizza_size,
        'pizza_crust': pizza_crust,
        'pizza_sauce': pizza_sauce,
        'pizza_cheese': pizza_cheese,
        'toppings': toppings,
        'last_four_digits': last_four_digits
    })