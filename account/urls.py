from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login',views.LoginView.as_view(),name='login'),
    path('register',views.OtpLoginView.as_view(),name='register'),
    path('checkotp',views.CheckOtpView.as_view(),name='check_otp'),
]