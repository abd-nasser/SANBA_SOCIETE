from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .utils import send_mail_with_body_html
from .form import ClientForm


def register_view(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            email = form.cleaned_data.get("email")
            send_mail_with_body_html(
                subject="Inscription Reussi",
                recipient_list=[email],
                template="mail.html",
                context={"username":form.cleaned_data.get("username")}
            )
            return redirect("home_app:home")
            
        else:
            ctx = {"form": form}
            return render (request, "auth_templates/register.html", ctx)
    else:
        ctx = {"form": ClientForm()}
        return render(request,"auth_templates/register.html",ctx)
            
            
            
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home_app:home")
        else:
            ctx = {"form":form}
            return render(request, "auth_templates/login.html", ctx)
    else:
        ctx= {"form":AuthenticationForm()}
        return render(request,"auth_templates/login.html",ctx)
    
    
    
def logout_view(request):
    logout(request)
    return redirect("home_app:home")
    
    
    