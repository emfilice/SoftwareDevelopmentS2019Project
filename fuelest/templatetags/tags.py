from django import template
from fuelest.forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

register = template.Library()

@register.simple_tag(takes_context=True)
def number_of_messages(context):
    request = context['request']
    userprof = UserInfo.objects.filter(username=User.objects.get(username=request.user.username))
    profile_made = (len(userprof) != 0)
    return profile_made
