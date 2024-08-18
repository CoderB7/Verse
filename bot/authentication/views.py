from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse

from bot.models import OTP
from bot.forms import OTPForm

from account.models import CustomUser
from bot.models import TelegramUser

import json

def check_telegram_user(username, telegram_user):
    print('checking_2')
    try:
        if telegram_user.django_user.username == username:
            return False # telegram user is true with django user
        elif telegram_user.django_user:
            return True # telegram user is already bound with different django user
    except TelegramUser.django_user.RelatedObjectDoesNotExist:
        return False  


def check_django_user(username, telegram_user):
    print('checking')
    try:
        user = get_object_or_404(CustomUser, username=username)
        if user.telegram_user:
            if telegram_user == user.telegram_user:
                return user # user telegram_user found
            else:
                return False # user found and telegram already bound
        else:
            user.telegram_user = telegram_user # user found but no telegram_user bound
    except Http404:
        user = CustomUser.objects.create_user(username=username, telegram_user=telegram_user)
        user.save() # user created with telegram_user
        
    return user


@csrf_exempt
def otp_login(request):
    if request.method == 'POST':
        print(json.loads(request.body))
        otp_code = json.loads(request.body)['otp']
        username = json.loads(request.body)['username']
        print(f"OTP value: {otp_code}")
        print(f"Username: {username}")
        if otp_code:
            if username:
                try:
                    otp = OTP.objects.get(code=otp_code, active_till__gte=timezone.now())
                    telegram_user = otp.user
                    is_bound = check_telegram_user(username, telegram_user)
                    if is_bound:
                        return JsonResponse({"status": "error", "message": f"This telegram user called {telegram_user} is bound already to user called {telegram_user.django_user}!"}, status=404)    
                    user = check_django_user(username, telegram_user)
                    if user == False:
                        return JsonResponse({"status": "error", "message": f"Only one Telegram user can be used with this user called {username}!"}, status=404)
                    elif user:
                        login(request, user)
                        return redirect('dashboard-channels')
                    else:
                        messages.error(request, "Invalid OTP or OTP has expired.")
                except OTP.DoesNotExist:
                    messages.error(request, "Invalid OTP or OTP has expired.") 
            else:
                messages.error(request, 'Username field can not be empty!')
                
        else:
            messages.error(request, 'Please provide OTP code!')
            
    else:
        pass
    return render(request, 'account/otp_login.html')
