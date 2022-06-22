from django.forms import ModelForm
from box.models import *
from django import forms


# FORM TO ADD IDEA
class CreateIdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # self.nom = kwargs.pop('nom', None)
        # self.description = kwargs.pop('description', None)
        # self.theme = kwargs.pop('theme', None)
        # self.categorie = kwargs.pop('categorie', None)

        super(CreateIdeaForm, self).__init__(*args, **kwargs)
        theme = Theme.objects.first()
        categorie = Categorie.objects.filter(theme=theme).first()

        self.fields['nom'] = forms.CharField(
            label="Nom",
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            help_text='Saisis ton prénom ou surnom')

        self.fields['description'] = forms.CharField(
            label="Description",
            required=False,
            widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            help_text='Saisis ton idée !')

        self.fields['theme'] = forms.ModelChoiceField(
            label="Theme",
            queryset=Theme.objects.all(),
            required=True,
            initial=theme,
            widget=forms.Select(attrs={'class': 'form-control'}),
            help_text='Choisir un theme')

        self.fields['categorie'] = forms.ModelChoiceField(
            label="Categorie",
            queryset=Categorie.objects.all(),
            required=True,
            initial=categorie,
            widget=forms.Select(attrs={'class': 'form-control'}),
            help_text='Choisir une catégorie')

    class Meta:
        model = Idea
        fields = ['nom', 'description', 'theme', 'categorie']
