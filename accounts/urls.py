from django.urls import path
from accounts import views

urlpatterns = [
    # ---- User ----
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('verify-accounts/<str:token>/', views.verify_email, name='verify_email'),
    path('send_otp/<str:email>/', views.send_otp, name='send_otp'),
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('vendor-register/', views.vendor_register_page, name='vendor_register'),
    path('vendor-login/', views.vendor_login_page, name='vendor_login'),
    
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor-verify/<str:token>/', views.verify_vendor_email, name='verify_vendor_email'),
    path('vendor-send-otp/<str:email>/', views.send_otp_vendor, name='vendor_send_otp'),
    path('vendor-verify-otp/<str:email>/', views.verify_otp_vendor, name='verify_otp_vendor'),
]
