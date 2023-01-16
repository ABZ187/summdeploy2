from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import ColdCoffee, Subscription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CoffeePaymentForm(forms.ModelForm):
    class Meta:
        model = ColdCoffee
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'amount',
            'email',
            Submit('submit', 'Next', css_class='button white btn-block btn-primary')
        )


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Next', css_class='button white btn-block btn-primary')
        )
