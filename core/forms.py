from django import forms

from .models import Task, User, TaskStep
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  

class TaskForm(forms.ModelForm):
    required_css_class = 'required_field'
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "block w-full p-2 text-gray-900 border border-gray-300 rounded-l"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "py-10 px-10 block w-full p-4 text-gray-900 border border-gray-300 rounded-l"}))
    complete = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "my-3 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300"}))
    class Meta:
        model = Task
        fields = ['title', 'user_date', 'description', 'complete']
        widgets = {
            'user_date': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TaskStepForm(forms.ModelForm):
     class Meta:
        model = TaskStep
        fields = ('step',)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

TaskFormSet = inlineformset_factory(Task, TaskStep, form=TaskStepForm, fields=('__all__'), can_delete=False,  extra=5, widgets = {'step': forms.Textarea(attrs={"class": "h-12 min-h-12 max-h-12 block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 "})})