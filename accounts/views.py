from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.shortcuts import render, redirect, HttpResponseRedirect

from IdeaBox.settings import DEBUG
from accounts.models import *
from accounts.forms import UsersLoginForm, UsersChangeForm
from datetime import datetime
import logging
from accounts.core import *

logger = logging.getLogger(__name__)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print(username, "s'est connecté(e) @", datetime.now())
        logger.info(str(username) + " s'est connecté(e)")
        return redirect("/")
    return render(request, "accounts/login.html", {"form": form, "title": "Identification", })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def forget_view(request):
    form = UsersLoginForm(request.POST or None)
    user = None
    if request.method == "POST":
        username = request.POST['username']
        user_html = ""
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                if user.first_name != "":
                    user_html = user.first_name
                else:
                    user_html = user.username
            except:
                user = None
        else:
            try:
                user = User.objects.get(username=username)
                if user.first_name != "":
                    user_html = user.first_name
                else:
                    user_html = user.username
                if user.email == "":
                    messages.error(request, "Aucun email n'est enregistré pour ce compte !")
                    return redirect('forget-support')
            except:
                user = None
        if user is None:
            messages.error(request, "Un problème est survenu ... compte inexistant !")
            return redirect('forget')

        token_mail = generate_random_token(40)
        create_token = TokenLogin.objects.create(token=token_mail, user=user)

        if DEBUG is True:
            href = "http://127.0.0.1:8000/accounts/reset/" + str(user.id) + "/" + str(token_mail)
        else:
            href = "https://apelndtg.pythonanywhere.com/accounts/reset/" + str(user.id) + "/" + str(token_mail)

        email_html = "<br/><br/>Bonjour " + user_html + ",<br/><br/>"
        email_html += "Tu viens de faire une demande de réinitialisation de mot de passe sur le site <a href='http://apelndtg.pythonanywhere.com'>APEL @ ENDTG</a><br>"
        email_html += "Cliques sur le lien ci-dessous afin de pouvoir changer ton mot de passe <br/><br/>"
        email_html += "<a href='" + href + "'>Changer mon mot de passe</a><br/><br/>"
        email_html += "Si tu n'es pas à l'origine de cette demande, merci ne pas tenir compte de ce mail.<br/><br/>"
        email_html += "Equipe Support - APEL @ ENDTG"
        print("User mail to user : ", user.email)
        send_mail("APEL @ ENDTG - Mot de passe oublié", email_html, '', '', user.email, '')

        messages.success(request, "Un email vient de t'être envoyé !")
        return redirect("login")
        # user = authenticate(request, username=username, password=password)

    context = {
        'form': form,
    }
    return render(request, "accounts/forget.html", context)


def reset_password(request, user, token):
    try:
        user = User.objects.get(id=user)
    except:
        messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
        return redirect("login")
    try:
        token = TokenLogin.objects.get(user=user, token=token)
    except:
        messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
        return redirect("login")

    if request.POST:
        if request.POST.get('pass1') == request.POST.get('pass2') and request.POST.get('pass1') != "":
            user = request.POST.get('user')
            try:
                user = User.objects.get(id=user)
            except:
                messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
                return redirect("login")

            user.set_password(request.POST.get('pass1'))
            user.save()
            token.delete()

            if DEBUG is True:
                href = "http://127.0.0.1:8000/accounts/login"
                # href = "https://endtg.pythonanywhere.com/accounts/login"
            else:
                href = "https://apelndtg.pythonanywhere.com/accounts/login"

            email_html = "<br/><br/>Bonjour " + user.username + ",<br/><br/>"
            email_html += "Tu viens de modifier ton mot de passe pour accéder au site <a href='http://apelndtg.pythonanywhere.com'>APEL @ ENDTG</a><br>"
            email_html += "Cliques sur le lien ci-dessous afin de pouvoir t'identifier.<br/><br/>"
            email_html += "<a href='" + href + "'>Identification</a><br/><br/>"
            email_html += "Si tu n'es pas à l'origine de cette demande, merci de me contacter afin que l'on puisse te réinitialiser ton mot de passe.<br/><br/>"
            email_html += "Equipe Support - APEL @ ENDTG"
            print("User mail to user : ", user.email)
            send_mail("APEL @ ENDTG - Nouveau mot de passe", email_html, '', '', user.email, '')

            messages.success(request, format_html("Votre mot de passe a bien été réinitialisé."))
            return redirect("login")
        else:
            messages.error(request, format_html("Les mots de passe ne correspondent pas !<br> Merci de réessayer."))
            return redirect('reset', user.id, token.token)

    context = {
        'user_reset': user,
        'token': token.token,
    }
    return render(request, "accounts/reset.html", context)


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


def forget_support_view(request):
    context = {}
    return render(request, 'accounts/forget_support.html', context)


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
