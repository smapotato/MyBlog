from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, RegisterForm


def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_form = LoginForm()
    context = {
        "login_form": login_form
    }
    return render(request, "user/login.html", context=context)


@csrf_exempt
def login_for_modal(request):
    # 模态框登录
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        data = {}
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            auth.login(request, user)
            data["status"] = "SUCCESS"
        else:
            data["status"] = "ERROR"
        return JsonResponse(data)


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            email = register_form.cleaned_data["email"]
            password = register_form.cleaned_data["password"]
            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # 登录用户
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        register_form = RegisterForm()
    context = {
        "register_form": register_form
    }
    return render(request, "user/register.html", context=context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get("from", reverse("home")))