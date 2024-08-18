from django.urls import path
from .views import register, logout, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]
