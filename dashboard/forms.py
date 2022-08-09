
from dataclasses import fields
from django import forms
from .models import Notes, Homework, Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "desciption"]


class DateInput(forms.DateInput):
    input_type = "date"

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {
            "due": DateInput()
        }
        fields = ["subject","due","desciption","title",'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200, label="Enter your search:")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title","is_finished"]


class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),("mass","Mass")]
    measurment = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [("yard","Yard"),("foot","Foot")]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))


class ConversionMassForm(forms.Form):
    CHOICES = [("pound","Pound"),("kilogram","Kilogram")]
    input = forms.CharField(required=False, label=False, widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))


class UserRegistrationForm(UserCreationForm):
    class meta:
        model = User
        fields = ["username", "password1", "password2"]
