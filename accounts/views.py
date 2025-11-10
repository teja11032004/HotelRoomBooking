from django.shortcuts import render,redirect
from .models import HotelUser
from django.db.models import Q
from django.contrib import messages
from .utils import generateToken , sendEmailToken,sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import random

def login_page(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(email=email)

        if not hotel_user.exists():
            messages.warning(request,"no Account Found")
            return redirect("accounts/login")
        
        if not hotel_user[0].is_verified:
            messages.warning(request,"Account not verified")
            return redirect("accounts/login")
        
        hotel_user=authenticate(username=hotel_user[0].username,password=password)
        
        if hotel_user:
            messages.success(request,"Login Success")
            login(request,hotel_user)
            return redirect("/accounts/login")
        
        messages.warning(request,"invalid Creditials")
        return redirect("/accounts/login")

    return render(request,'login.html')

def register_page(request): 
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        password=request.POST.get('password')

        hotel_user=HotelUser.objects.filter(
            Q(email=email) | Q(phone_number=phone)
        )

        if hotel_user.exists():
            messages.success(request,"Already account exists")
            return redirect('/accounts/register')
        
        hotel_user=HotelUser.objects.create(
            username=name,
            email=email,
            phone_number=phone,
            email_token=generateToken()

        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email,hotel_user.email_token)

        messages.success(request,"Email sent!!")
        return redirect('/accounts/register')

    return render(request,'register.html')


def verify_email(request,token):
    try:
        hotel_user=HotelUser.objects.get(email_token=token)
        hotel_user.is_verified=True
        hotel_user.save()
        messages.success(request,"Email Verified")
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponse("Invalid Token")
    
def send_otp(request, email):
    try:
        hotel_user = HotelUser.objects.get(email=email)
    except HotelUser.DoesNotExist:
        messages.warning(request, "No Account Found")
        return redirect('/accounts/login/')
    
    otp = random.randint(1000, 9999)
    hotel_user.otp = otp
    hotel_user.save()

    sendOTPtoEmail(email, otp)
    return redirect(f'/accounts/verify-otp/{email}/')



def verify_otp(request,email):
    if request.method == "POST":
        otp=request.POST.get('otp')
        hotel_user=HotelUser.objects.get(email=email)
        if otp==hotel_user.otp:
            messages.success(request,"Login Success")
            login(request,hotel_user)
            return redirect(f'/accounts/login/')
        messages.warning(request,"Wrong OTP")
        return redirect(f"/accounts/verify-otp/{email}/")
    
    return render(request,'verify_otp.html')


