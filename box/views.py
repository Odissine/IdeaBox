from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

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


def create_idea(request):
    form = CreateIdeaForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Idée ajoutée avec succès !')
            return redirect('index')

    context = {'form': form}
    return render(request, 'box/idea.html', context)


def edit_idea(request, idea):
    obj = None
    if idea is not None:
        obj = Idea.objects.get(pk=idea)
    form = CreateIdeaForm(request.user, request.POST or None, instance=obj)
    if request.method == 'POST':
        form = CreateIdeaForm(request.user, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # dt = pytz.timezone("FRA").localize(datetime.now(), is_dst=None)
            obj.last_modified = timezone.now()
            obj.save()
            messages.success(request, 'Idée modifiée avec succès !')
            return redirect('index')
    context = {'form': form, 'idea': obj}
    return render(request, 'box/idea.html', context)


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

            return JsonResponse({'like': idea.like, 'thumb': thumb})
        except:
            return False
