from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import (LoginView)

from .forms import UserRegistrationForm, LoginForm

def register(request):
    is_auth_page = True
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            # Profile.objects.create(user=new_user)
            messages.success(request, "Your account has been created! You are now able to login")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form, 'is_auth_page': is_auth_page})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = LoginForm
    next_page = 'dashboard-channels'
    is_auth_page = True

    def get(self, request, *args, **kwargs):
        context = locals()
        context['form'] = self.authentication_form
        context['is_auth_page'] = self.is_auth_page
        context['next_page'] = self.next_page
        return render(request, self.template_name, context)
    
def logout(request):
    if request.method == 'GET':
        django_logout(request)
        return render(request, 'user_verse/main_page.html')
