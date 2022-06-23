from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.forms import UsersLoginForm, UsersChangeForm
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


def forget_view(request):
    return redirect("/")


@login_required
def preferences_view(request):
    form = UsersChangeForm(request.user, request.POST or None, instance=request.user)
    if request.POST:
        if form.is_valid():
            user = form.save()
            message = "Profil modifié avec succès !"
            messages.success(request, message)
            return redirect('preferences')
        else:
            print(form.errors)
            message = "Une erreur s'est produit lors de la mise à jour !"
            messages.error(request, message)
            return redirect('preferences')
    context = {
        'form': form,
    }
    return render(request, 'accounts/preferences.html', context)


def help_view(request):
    return redirect("/")


@login_required
def password_reset(request):
    if request.POST:
        password = request.POST.get("currentPassword")
        newpassword = request.POST.get("newPassword")
        confirmpassword = request.POST.get("renewPassword")
        if request.user.check_password(password):
            if newpassword == confirmpassword:
                request.user.set_password(password)
                request.user.save()
                message = "Mot de passe modifié avec succès !"
                messages.success(request, message)
                return redirect('preferences')
            else:
                message = "La confirmation du mot de passe ne correspond pas au mot de passe saisie !"
                messages.error(request, message)
                return redirect('preferences')
        else:
            message = "L'ancien mot de passe n'est le bon !"
            messages.error(request, message)
    context = {
    }
    return render(request, 'accounts/preferences.html', context)
