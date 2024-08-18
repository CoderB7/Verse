from django import forms
from django.contrib.auth.models import User
from account.models import CustomUser

class OTPForm(forms.Form):

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

    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}),
        label='OTP Code'
    )
    
    class Meta:
        model = CustomUser
        

    def __init__(self, *args, **kwargs):
        super(OTPForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = None

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if not otp_code.isdigit():
            raise forms.ValidationError('OTP code must be numeric.')
        return otp_code
    
    def clean_username(self):
        data = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already in use.')
        return data
    