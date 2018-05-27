from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        print(username)
        password = self.cleaned_data.get("password")

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("用户名或密码不正确")
        else:
            self.cleaned_data["user"] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)
    password_again = forms.CharField(min_length=6)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")

    def clean_password_again(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if password != password_again:
            raise forms.ValidationError("两次输入的密码不一致")
        return password_again
