from django.urls import path
from accounts import views

urlpatterns = [
    path('login/',views.login_page,name="login_page"),
    path('register/',views.register_page,name='register_page'),
    path('send_otp/<email>/',views.send_otp,name='send_otp'),
    path('verify-otp/<email>/',views.verify_otp,name='verify_otp'),
    path('verify-accounts/<token>/',views.verify_email,name="verify_email")

  
]