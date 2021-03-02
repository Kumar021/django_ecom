from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

def logout_view(request):
    logout(request) 
    return redirect('products:list')


def guest_register_page(request):
    print("guest register view")
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    # print("User logged in")
    #print(request.user.is_authenticated())
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    print("redirect_path guest:",redirect_path)
    if form.is_valid():
        name  = form.cleaned_data.get("name")
        email  = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(name=name, email=email)
        request.session['new_guest_email'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")

    return redirect("/register/")


def login_page(request):
    print("login view")
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    # print("User logged in")
    #print(request.user.is_authenticated())
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    #print(redirect_path)
    if form.is_valid():
        # print(form.cleaned_data)
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        # print(user)
        #print(request.user.is_authenticated())
        if user is not None:
            #print(request.user.is_authenticated())

            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error")

    return render(request, "accounts/login.html", context)





def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username  = form.cleaned_data.get("username")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        new_user  = User.objects.create_user(username, email, password)
        print(new_user)

    return render(request, "accounts/register.html", context)