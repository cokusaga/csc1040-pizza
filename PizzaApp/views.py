from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
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

def logout_view(request):
    logout(request)
    return redirect('index')

# Dashboard view
@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)  # Get orders for logged-in user
    return render(request, 'dashboard.html', {'orders': orders})

# Create pizza view
@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = PizzaOrderForm(request.POST)
        if form.is_valid():
            print("Form is valid!")
            pizza_order = form.save(commit=False)
            pizza_order.user = request.user
            pizza_order.save()

            form.save_m2m()  # Save many-to-many toppings
            print(f"Created order with ID: {pizza_order.id}")  # Debugging line to check the order ID
            return redirect('payment', order_id=pizza_order.id)  # Redirect to payment page
        else:
            print("Form is not valid!")  # Debugging line to indicate the form isn't valid
            print(form.errors)  # Print out the form errors in the console
            messages.error(request, "Error creating order. Please check your form.")
    else:
        form = PizzaOrderForm()

    print("Render create_pizza page")  # Debugging line to indicate render is happening
    return render(request, 'create_pizza.html', {'form': form})

# Payment view
@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        form = DeliveryDetailsForm(request.POST, instance=order)
        if form.is_valid():
            # Handle the payment form and save delivery info
            order.full_name = form.cleaned_data['full_name']
            order.delivery_address = form.cleaned_data['delivery_address']
            order.save()

            messages.success(request, "Payment details saved successfully!")
            return redirect('order_confirmation', order_id=order.id)
        else:
            # The form is invalid, so we rely on the form's error messages
            messages.error(request, "Invalid form submission. Please check your details.")
    else:
        form = DeliveryDetailsForm(instance=order)

    return render(request, 'payment.html', {'form': form, 'order': order})

# Order confirmation view
@login_required
def order_confirmation(request, order_id):
    print(f"Fetching order with ID: {order_id}")  # Debug: Check if the correct order ID is passed
    order = get_object_or_404(Order, id=order_id, user=request.user)

    pizza_size = order.pizza_size.name if order.pizza_size else "No size selected"
    pizza_crust = order.pizza_crust.name if order.pizza_crust else "No crust selected"
    pizza_sauce = order.pizza_sauce.name if order.pizza_sauce else "No sauce selected"
    pizza_cheese = order.pizza_cheese.name if order.pizza_cheese else "No cheese selected"
    toppings = order.toppings.all()

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
