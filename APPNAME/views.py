from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Password
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
import random

fernet = Fernet(settings.KEY)
br = Browser()
br.set_handle_robots(False)

global_code = None
global_username = None

def home(request):
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.filter(user=request.user)
        for p in passwords:
            p.email = fernet.decrypt(p.email.encode()).decode()
            p.password = fernet.decrypt(p.password.encode()).decode()
        context["passwords"] = passwords

    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            messages.success(request, "Logged out.")
            return redirect("home")

        elif "delete" in request.POST:
            pid = request.POST.get("password-id")
            Password.objects.get(id=pid).delete()
            messages.success(request, "Password deleted.")
            return redirect("home")

        elif "login-form" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                global global_code, global_username
                global_username = username
                global_code = str(random.randint(100000, 999999))

                send_mail(
                    "2FA Verification - Django Password Manager",
                    f"Your 6-digit code: {global_code}",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                return render(request, "email_verification.html", {"user": user})
            else:
                messages.error(request, "Invalid login.")
                return redirect("home")

    return render(request, "home.html", context)

def confirm_code(request):
    global global_code, global_username

    if request.method == "POST":
        input_code = request.POST.get("code")
        username = request.POST.get("user")

        if input_code == global_code and username == global_username:
            try:
                user = User.objects.get(username=username)
                login(request, user)
                messages.success(request, "2FA successful. Logged in.")
                return redirect("home")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid code.")

    return redirect("home")

def signup_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Signup successful.")
            return redirect("home")

    return render(request, "signup.html")

def add_password(request):
    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        url = request.POST.get("url")
        email = request.POST.get("email")
        password = request.POST.get("password")

        encrypted_email = fernet.encrypt(email.encode())
        encrypted_password = fernet.encrypt(password.encode())

        try:
            br.open(url)
            title = br.title()
        except:
            title = url

        try:
            icon = favicon.get(url)[0].url
        except:
            icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"

        Password.objects.create(
            user=request.user,
            name=title,
            logo=icon,
            email=encrypted_email.decode(),
            password=encrypted_password.decode()
        )

        messages.success(request, f"{title} saved.")
        return redirect("home")

    return render(request, "add_password.html")

def update_password(request, id):
    if not request.user.is_authenticated:
        return redirect("home")

    password_entry = get_object_or_404(Password, id=id, user=request.user)

    if request.method == "POST":
        new_email = request.POST.get("email")
        new_password = request.POST.get("password")
        new_url = request.POST.get("url")

        encrypted_email = fernet.encrypt(new_email.encode())
        encrypted_password = fernet.encrypt(new_password.encode())

        try:
            br.open(new_url)
            title = br.title()
        except:
            title = new_url

        try:
            icon = favicon.get(new_url)[0].url
        except:
            icon = password_entry.logo

        password_entry.name = title
        password_entry.email = encrypted_email.decode()
        password_entry.password = encrypted_password.decode()
        password_entry.logo = icon
        password_entry.save()

        messages.success(request, "Password updated successfully.")
        return redirect("home")

    password_entry.email = fernet.decrypt(password_entry.email.encode()).decode()
    password_entry.password = fernet.decrypt(password_entry.password.encode()).decode()
    return render(request, "update_password.html", {"password": password_entry})
