from django import forms
from django.core.validators import RegexValidator

class PhoneCheckForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r'^(\+7|7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        message="Номер должен быть в формате: '+79991234567' или '89991234567'"
    )
    
    phone_number = forms.CharField(
        label='Номер телефона',
        max_length=20,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'placeholder': '+79991234567',
            'class': 'form-control'
        })
    )
    
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        # Дополнительная очистка номера
        return ''.join(c for c in phone if c.isdigit())