from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'

        for fieldname in ['username', 'email']:  # to remove help_text
            self.fields[fieldname].help_text = None

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

class LoginForm(AuthenticationForm):  # AuthenticationForm for updating it for LoginView
    # username = None  # to remove the requirement for the "username" field.

    username = forms.CharField(  # expects both email and username
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username/Email',
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
                'placeholder': 'Password'
            }
        )
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct email/username and password."
        ),
        'inactive': (
            "This account is inactive."
        ),
    }

    def clear(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data

