from django.urls import path
from accounts import views

urlpatterns = [
    path('login/',views.login_page,name="login_page"),
    path('register/',views.register_page,name='register_page'),
    path('verify-accounts/<token>/',views.verify_email,name="verify_email")

  
]