from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import Order
from .models import Profile

class UserForm(UserCreationForm):
    #email = forms.EmailField()

    class Meta:
        model = User
        #fields = ['username', 'first_name', 'email', 'password1', 'password2']
        fields = ['username', 'first_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phonenumber', 'address']
        # widgets = {
        #     'birthdate': DateInput(attrs={'type': 'date'}),
        # }