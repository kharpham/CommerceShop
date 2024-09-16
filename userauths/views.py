from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from userauths.forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.conf import settings
from userauths.models import User

# User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}, your account has been created successfully!")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()
    context = {
        'form': form 
    }
    return render(request, "userauths/sign-up.html", context=context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")  
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try: 
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User does not exist")
        except:
            messages.warning(request, f"User with {email} doesn't exist")

    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("userauths:sign-in")

@login_required()
def profile_update(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.verified = True
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("core:dashboard")
    print(profile)
    form = ProfileUpdateForm(instance=profile)
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "userauths/profile-update.html", context)
