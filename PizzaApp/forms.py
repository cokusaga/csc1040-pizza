from django import forms
from .models import Order, PizzaSize, PizzaCrust, PizzaSauce, PizzaCheese, PizzaTopping
from datetime import datetime

class PizzaOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pizza_size', 'pizza_crust', 'pizza_sauce', 'pizza_cheese', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple(),  # For multiple toppings, use checkboxes
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load choices for size, crust, sauce, and cheese from the database
        self.fields['pizza_size'].queryset = PizzaSize.objects.all()
        self.fields['pizza_crust'].queryset = PizzaCrust.objects.all()
        self.fields['pizza_sauce'].queryset = PizzaSauce.objects.all()
        self.fields['pizza_cheese'].queryset = PizzaCheese.objects.all()
        self.fields['toppings'].queryset = PizzaTopping.objects.all()


class DeliveryDetailsForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Full Name"
    )

    class Meta:
        model = Order
        fields = ['full_name', 'delivery_address', 'card_number', 'card_expiry_date', 'card_cvv']

    def clean_card_number(self):
        """ Validate and mask card number """
        card_number = self.cleaned_data.get('card_number')
        
        if not card_number.isdigit():
            raise forms.ValidationError("Card number must contain only digits.")
        
        if len(card_number) not in [13, 15, 16]:  # Common lengths for Visa, Mastercard, Amex
            raise forms.ValidationError("Invalid card number length.")

        return card_number

    def clean_card_expiry_date(self):
        """ Validate card expiry date format MM/YY and check if it's in the future """
        card_expiry = self.cleaned_data.get('card_expiry_date')

        if not card_expiry or len(card_expiry) != 5 or card_expiry[2] != '/':
            raise forms.ValidationError("Invalid expiration date format. Use MM/YY.")

        # Check if expiry is in the future
        try:
            exp_month, exp_year = map(int, card_expiry.split('/'))
            exp_year += 2000  # Convert YY to YYYY format
            current_year = datetime.now().year
            current_month = datetime.now().month

            if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                raise forms.ValidationError("Card has expired.")

        except ValueError:
            raise forms.ValidationError("Invalid expiration date.")

        return card_expiry

    def clean_card_cvv(self):
        """ Validate CVV """
        card_cvv = self.cleaned_data.get('card_cvv')

        if not card_cvv.isdigit():
            raise forms.ValidationError("CVV must contain only digits.")
        
        if len(card_cvv) not in [3, 4]:  # 3 for Visa/Mastercard, 4 for Amex
            raise forms.ValidationError("Invalid CVV length.")

        return card_cvv