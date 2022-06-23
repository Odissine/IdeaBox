from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User


class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', "name": "username"})
        self.fields['password'].widget.attrs.update({'class': 'form-control', "name": "password"})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Mot de passe ou nom d'utilisateur inccorect !")

        return super(UsersLoginForm, self).clean(*args, **keyargs)


class UsersChangeForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        super(UsersChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', "name": "username"})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', "name": "first_name"})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', "name": "last_name"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', "name": "email"})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
