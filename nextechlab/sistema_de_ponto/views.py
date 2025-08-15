from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Aluno, Professor, RegistroPontoAluno
from .forms import UserForm, LoginForm


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sistema_de_ponto/index.html")


def user_register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        forms = UserForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return HttpResponse("User registered successfully.")
    else:
        forms = UserForm()
    return render(request, "sistema_de_ponto/user_register.html", {"form": forms})


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Login successful.")
            else:
                return HttpResponse("Invalid username or password.")
        else:
            return HttpResponse("Invalid form data.")
    else:
        form = LoginForm()
    return render(request, "sistema_de_ponto/login.html", {"form": form})
