from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# создание формы
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'popup_input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e-mail', 'class': 'popup_input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'popup_input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, label='Телефонный номер')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number']

    def save(self, commit=True):
        # Сначала сохраняем пользователя
        user = super().save(commit=False)
        
        if commit:
            user.save()  # Сохраняем пользователя
        
        # Сохраняем телефонный номер в профиль
        phone_number = self.cleaned_data.get('phone_number')
        Profile.objects.create(user=user, phone_number=phone_number)  # Создаем профиль с номером телефона
        
        return user