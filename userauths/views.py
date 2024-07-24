from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from userauths.forms import UserRegisterForm
from django.contrib import messages


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
        