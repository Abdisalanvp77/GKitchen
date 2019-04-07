from django import forms
from django.core import validators
from django.contrib.auth.forms import AuthenticationForm

from . models import Contacted
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
  password = forms.CharField(label="Password", widget=forms.PasswordInput())
  passwordconfirm = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())
  class Meta():
    model = User
    fields = ('first_name','last_name','username','email','password','passwordconfirm')
  # this function will be used for the validation 
  def clean(self): 

    form_data = self.cleaned_data
    if form_data['password'] != form_data['passwordconfirm']:
        self._errors["password"] = ["Passwords do not match"] # Will raise a error message
        del form_data['password']
    return form_data



class UserLogin(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    ("Email ou Senha errados"))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(("This account is inactive."))
        return self.cleaned_data


class ContactedPeople(forms.ModelForm):
    firstName = forms.CharField(label='First Name')
    lastName = forms.CharField(label='Last Name')
    contactEmail = forms.EmailField(label='Your Email')
    subjectAreaText = forms.CharField(label='Comment', widget=forms.Textarea)

    class Meta():
        model = Contacted
        fields = ('firstName', 'lastName', 'contactEmail', 'subjectAreaText')

    def clean_email(self):
        email = self.cleaned_data.get('contactEmail')
        if email == "":
            raise forms.ValidationError("Email is required. Please fill it")
        return email
