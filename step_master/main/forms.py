from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'popup_input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e-mail', 'class': 'popup_input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'popup_input'}),
        } 