from django.forms import ModelForm
from ckeditor_uploader.widgets import *
from ckeditor.fields import RichTextField

from box.models import Idea as IdeaModel, Theme as ThemeModel, Categorie as CategorieModel
from django import forms


# FORM TO ADD IDEA
class CreateIdeaForm(ModelForm):


    theme = ThemeModel.objects.first()
    categorie = CategorieModel.objects.filter(theme=theme).first()

    nom = forms.CharField(
        label="Prénom",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Saisis ton prénom'}),
        help_text='Saisis ton prénom ou surnom')

    description = RichTextField()
            # label="Description",
            # required=False,
            # widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            # widget=CKEditorUploadingWidget(),
            # help_text='Saisis ton idée !')

    theme = forms.ModelChoiceField(
            label="Theme",
            queryset=ThemeModel.objects.all(),
            required=True,
            initial=theme,
            widget=forms.Select(attrs={'class': 'form-select'}),
            help_text='Choisir un theme')

    categorie = forms.ModelChoiceField(
            label="Categorie",
            queryset=CategorieModel.objects.all(),
            required=True,
            initial=categorie,
            widget=forms.Select(attrs={'class': 'form-select'}),
            help_text='Choisir une catégorie')

    class Meta:
        model = IdeaModel
        fields = ['nom', 'description', 'theme', 'categorie']
