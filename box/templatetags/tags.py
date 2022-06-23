from django import template
from box.models import *

register = template.Library()


def check_like(user, idea):
    check = UserLike.objects.filter(user=user, idea=idea)
    if len(check)>0:
        return True
    return False


def get_users_like(idea):
    likes = UserLike.objects.filter(idea=idea)
    data = "<span class='text-start'>"
    for like in likes:
        data = data + str(like.user.username) + "</br>"
    data = data + "</span>"
    return data


register.filter('check_like', check_like)
register.filter('get_users_like', get_users_like)