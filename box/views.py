from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from box.models import *
from box.forms import *
from datetime import datetime
import pytz


def index(request, theme=None, categorie=None):
    themes = Theme.objects.all()
    categories = None
    ideas = Idea.objects.all()
    if theme is not None:
        categories = Categorie.objects.filter(theme=theme)
        theme = Theme.objects.get(pk=theme)
        ideas = Idea.objects.filter(theme=theme)
        if categorie is not None:
            categorie = Categorie.objects.get(pk=categorie)
            ideas = Idea.objects.filter(theme=theme, categorie=categorie)

    context = {'themes': themes, 'categories': categories, 'theme': theme, 'categorie': categorie, 'ideas': ideas}
    return render(request, 'box/index.html', context)


@login_required
def create_idea(request):
    form = CreateIdeaForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Idée ajoutée avec succès !')
            return redirect('index')

    context = {'form': form}
    return render(request, 'box/idea.html', context)


@login_required
def edit_idea(request, idea):
    obj = None
    if idea is not None:
        obj = Idea.objects.get(pk=idea)
        if obj.user != request.user and not request.user.is_staff:
            messages.error(request, "Tu ne peux pas modifier cette idée, ce n'est pas la tienne :)")
            return redirect('index')
    form = CreateIdeaForm(request.user, request.POST or None, instance=obj)
    if request.method == 'POST':
        form = CreateIdeaForm(request.user, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # dt = pytz.timezone("FRA").localize(datetime.now(), is_dst=None)
            obj.last_modified = timezone.now()
            obj.modified_user = request.user
            obj.save()
            messages.success(request, 'Idée modifiée avec succès !')
            return redirect('index')
    context = {'form': form, 'idea': obj}
    return render(request, 'box/idea.html', context)


@login_required
def delete_idea(request, idea):
    obj = None
    if idea is not None:
        obj = Idea.objects.get(pk=idea)
        if obj.user != request.user and not request.user.is_staff:
            messages.error(request, "Tu ne peux pas supprimer cette idée, ce n'est pas la tienne :)")
            return redirect('index')

        obj.delete()
        messages.success(request, 'Idée supprimée avec succès !')
        return redirect('index')
    return redirect('index')


@login_required
def like_idea(request):
    if request.POST:
        id_idea = request.POST.get('idea')
        print(id_idea)
        try:
            idea = Idea.objects.get(pk=id_idea)
            user_like = UserLike.objects.filter(idea=idea, user=request.user).first()
            if user_like:
                idea.like -= 1
                idea.save()
                user_like.delete()
                thumb = False
            else:
                idea.like += 1
                idea.save()
                obj = UserLike.objects.create(user=request.user, idea=idea)
                thumb = True

            likes = UserLike.objects.filter(idea=idea)
            likers = "<span class='text-start'>"
            for like in likes:
                likers = likers + str(like.user.username) + "</br>"
            likers = likers + "</span>"

            return JsonResponse({'like': idea.like, 'thumb': thumb, 'likers': likers})
        except:
            return False
