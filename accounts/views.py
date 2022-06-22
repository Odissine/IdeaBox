from django.contrib.auth import authenticate, login, logout
from accounts.forms import UsersLoginForm
from django.shortcuts import render, redirect, HttpResponseRedirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "accounts/login.html", {"form": form, "title": "Identification", })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
