from django.shortcuts import render
from userauths.forms import UserRegisterForm

# Create your views here.
def register_view(request):

    if request.method == 'POST':
        pass
    form = UserRegisterForm()
    context = {
        'form': form

    }
    return render(request, "userauths/sign-up.html", context=context)