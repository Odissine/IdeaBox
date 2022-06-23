from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class TimeStamped(models.Model):
    creation_date = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Theme(models.Model):
    objects = models.Manager()
    theme = models.CharField(max_length=255)
    color = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.theme


class Categorie(models.Model):
    objects = models.Manager()
    categorie = models.CharField(max_length=255)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=False, blank=False, related_name='Categories')

    def __str__(self):
        return self.categorie


class Idea(models.Model):
    objects = models.Manager()
    default_user = User.objects.filter(is_superuser=True).first()

    nom = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user.pk, related_name='Ideas')
    # description = models.TextField()
    description = RichTextField(blank=True,null=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=False, blank=False, related_name='Ideas')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=False, blank=False, related_name='Ideas')
    like = models.IntegerField(default=0)
    creation_date = models.DateTimeField(editable=False, auto_now_add=True)
    last_modified = models.DateTimeField(editable=False, null=True)
    modified_user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user.pk, related_name='ModifiedIdeas')


class UserLike(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='UserLikes')
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, null=False, related_name='UserLikes')
