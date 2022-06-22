"""IdeaBox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from box.views import *

urlpatterns = [
    path('', index, name='index'),
    path('box/idea/<theme>', index, name='idea'),
    path('box/idea/<theme>/<categorie>', index, name='idea'),
    path('box/create/', create_idea, name='create-idea'),
    path('box/edit/<idea>', edit_idea, name='edit-idea'),
    path('box/like', like_idea, name='like-idea'),
]
