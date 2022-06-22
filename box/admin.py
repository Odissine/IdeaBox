from django.contrib import admin
from .models import *


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['theme', 'color']


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['categorie', 'theme']
