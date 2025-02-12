from django import forms
from .models import Order, PizzaSize, PizzaCrust, PizzaSauce, PizzaCheese, PizzaTopping

class PizzaOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pizza_size', 'pizza_crust', 'pizza_sauce', 'pizza_cheese', 'toppings', 'full_name', 'delivery_address']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple(),  # For multiple toppings, use checkboxes
            'delivery_address': forms.Textarea(attrs={'placeholder': 'Enter delivery address'}),
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
    class Meta:
        model = Order
        fields = ['full_name', 'delivery_address', 'card_number', 'card_expiry_date', 'card_cvv']

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        delivery_address = cleaned_data.get('delivery_address')
        card_number = cleaned_data.get('card_number')
        card_expiry_date = cleaned_data.get('card_expiry_date')
        card_cvv = cleaned_data.get('card_cvv')

        # Validate full_name and delivery_address
        if not full_name:
            raise forms.ValidationError("Full name is required.")
        
        if not delivery_address:
            raise forms.ValidationError("Delivery address is required.")

        # Validate payment fields
        if not card_number or not card_expiry_date or not card_cvv:
            raise forms.ValidationError("All payment fields are required.")

        return cleaned_data
