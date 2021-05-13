from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class EventForm(forms.Form):
    name = forms.CharField(label='Event name', max_length=200)
    message = forms.CharField(label='Message you want to be displayed', max_length=200)
    date = forms.DateTimeField()
    has_reminder = forms.BooleanField(required=False)
    day_of_week = forms.IntegerField(required=False)
