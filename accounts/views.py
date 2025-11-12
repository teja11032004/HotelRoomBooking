from django.shortcuts import render, redirect
from .models import HotelUser, HotelVendor
from django.db.models import Q
from django.contrib import messages
from .utils import generateToken, sendEmailToken, sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required


# ------------------ USER LOGIN ------------------ #


def register_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        password = request.POST.get('password')

        if HotelUser.objects.filter(Q(email=email) | Q(phone_number=phone)).exists():
            messages.warning(request, "Account already exists.")
            return redirect('register_page')

        hotel_user = HotelUser.objects.create(
            username=name,
            email=email,
            phone_number=phone,
            email_token=generateToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()

        sendEmailToken(email, hotel_user.email_token)
        messages.success(request, "Verification email sent! Please check your inbox.")
        return redirect('login_page')
    return render(request, 'register.html')





def verify_email(request, token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email verified successfully! You can now login.")
        return redirect('login_page')
    except HotelUser.DoesNotExist:
        return HttpResponse("Invalid or expired verification token.")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            hotel_user = HotelUser.objects.get(email=email)
        except HotelUser.DoesNotExist:
            messages.warning(request, "No account found with that email.")
            return redirect("login_page")

        if not hotel_user.is_verified:
            messages.warning(request, "Account not verified. Please check your email.")
            return redirect("login_page")

        user = authenticate(username=hotel_user.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("login_page")  # redirect to home or dashboard
        else:
            messages.warning(request, "Invalid credentials.")
            return redirect("login_page")

    return render(request, 'login.html')


# ------------------ USER REGISTER ------------------ #



# ------------------ USER VERIFY EMAIL ------------------ #


# ------------------ USER SEND OTP ------------------ #
def send_otp(request, email):
    try:
        hotel_user = HotelUser.objects.get(email=email)
    except HotelUser.DoesNotExist:
        messages.warning(request, "No account found with that email.")
        return redirect('login_page')

    otp = random.randint(1000, 9999)
    hotel_user.otp = otp
    hotel_user.save()

    sendOTPtoEmail(email, otp)
    return redirect('verify_otp', email=email)


# ------------------ USER VERIFY OTP ------------------ #
def verify_otp(request, email):
    try:
        hotel_user = HotelUser.objects.get(email=email)
    except HotelUser.DoesNotExist:
        messages.warning(request, "No account found.")
        return redirect('login_page')

    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == str(hotel_user.otp):
            login(request, hotel_user)
            messages.success(request, "Login successful via OTP!")
            return redirect('login_page')
        else:
            messages.warning(request, "Incorrect OTP. Please try again.")
            return redirect('verify_otp', email=email)

    return render(request, 'verify_otp.html', {'email': email})


# ===================================================================== #
# ------------------ VENDOR REGISTER, LOGIN, OTP, VERIFY ---------------- #
# ===================================================================== #

def vendor_register_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        password = request.POST.get('password')

        if HotelVendor.objects.filter(Q(email=email) | Q(phone_number=phone)).exists():
            messages.warning(request, "Vendor account already exists.")
            return redirect('vendor_register')

        vendor = HotelVendor.objects.create(
            username=name,
            business_name=business_name,
            email=email,
            phone_number=phone,
            email_token=generateToken()
        )
        vendor.set_password(password)
        vendor.save()

        sendEmailToken(email, vendor.email_token)
        messages.success(request, "Verification email sent! Please verify before login.")
        return redirect('vendor_login')

    return render(request, 'vendor/vendor_register.html')

def vendor_login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            vendor = HotelVendor.objects.get(email=email)
        except HotelVendor.DoesNotExist:
            messages.warning(request, "No vendor account found.")
            return redirect('vendor_login')

        if not vendor.is_verified:
            messages.warning(request, "Please verify your email first.")
            return redirect('vendor_login')

        user = authenticate(username=vendor.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Vendor login successful!")
            return redirect('vendor_dashboard')  # ✅ fixed line
        else:
            messages.warning(request, "Invalid credentials.")
            return redirect('vendor_login')

    return render(request, 'vendor/vendor_login.html')



def verify_vendor_email(request, token):
    try:
        vendor = HotelVendor.objects.get(email_token=token)
        vendor.is_verified = True
        vendor.save()
        messages.success(request, "Vendor email verified successfully! Please login.")
        return redirect('vendor_login')
    except HotelVendor.DoesNotExist:
        return HttpResponse("Invalid or expired verification token.")


def send_otp_vendor(request, email):
    try:
        vendor = HotelVendor.objects.get(email=email)
    except HotelVendor.DoesNotExist:
        messages.warning(request, "No vendor account found.")
        return redirect('vendor_login')

    otp = random.randint(1000, 9999)
    vendor.otp = otp
    vendor.save()
    sendOTPtoEmail(email, otp)
    return redirect('verify_otp_vendor', email=email)


def verify_otp_vendor(request, email):
    try:
        vendor = HotelVendor.objects.get(email=email)
    except HotelVendor.DoesNotExist:
        messages.warning(request, "Vendor not found.")
        return redirect('vendor_login')

    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == str(vendor.otp):
            login(request, vendor)
            messages.success(request, "Vendor login successful!")
            return redirect('vendor_dashboard')
        else:
            messages.warning(request, "Incorrect OTP.")
            return redirect('verify_otp_vendor', email=email)

    return render(request, 'verify_otp.html', {'email': email})





@login_required(login_url='vendor_login')
def vendor_dashboard(request):
    return render(request, 'vendor/vendor_dashboard.html')
