from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse  # Corrección de HTTPResponse
from .forms import TaskForm

# Create your views here.


def home(request):
    return render(
        request, "home.html", {"form": UserCreationForm()}
    )  # Instanciando el formulario correctamente


def signup(request):

    if request.method == "GET":
        return render(
            request, "signup.html", {"form": UserCreationForm()}
        )  # Instanciando el formulario correctamente
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


def tasks(request):
    return render(request, "tasks.html")  # Crear la plantilla tasks.html


def create_tasks(request):
    if request.method == "GET":
        return render(request, "create_tasks.html", {"form": TaskForm()})
    else:


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
    if user is None:
        return render(
            request,
            "signin.html",
            {
                "form": AuthenticationForm,
                "error": "Username and password did not match.",
            },
        )
    else:
        # login(request, user) me guarda   la sesión del usuario
        login(request, user)
        return redirect("tasks")
