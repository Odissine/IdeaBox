from django import template
from box.models import *

register = template.Library()


def check_like(user, idea):
    check = UserLike.objects.filter(user=user, idea=idea)
    if len(check)>0:
        return True
    return False


register.filter('check_like', check_like)
