from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# ================= HOME =================
def home(req):
    return render(req, "home.html")

def tshirt(req):
    return render(req,"tshirt.html")


# ================= SIGNUP =================
def signup(req):

    if req.method == "POST":

        username = req.POST.get('username')
        email = req.POST.get('email')
        password1 = req.POST.get('password1')
        password2 = req.POST.get('password2')

        # password check
        if password1 != password2:
            messages.error(req, "Password does not match")
            return redirect('signup')

        # username exists
        if User.objects.filter(username=username).exists():
            messages.error(req, "Username already exists")
            return redirect('signup')

        # email exists
        if User.objects.filter(email=email).exists():
            messages.error(req, "Email already exists")
            return redirect('signup')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        messages.success(req, "Account created successfully")
        return redirect('login')

    return render(req, "signup.html")

def login(req):

    if req.method == 'POST':

        username = req.POST.get('username')
        password = req.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                req.session['username'] = user.username
                messages.success(req, 'login successfully')
                return redirect('home')
            else:
                messages.error(req, 'wrong password')
                return redirect('login')

        except:
            messages.error(req, 'user not found')
            return redirect('login')

    return render(req, 'login.html')

def logout(req):
    req.session.flush()
    messages.success(req, "Logged out successfully")
    return redirect('login')


