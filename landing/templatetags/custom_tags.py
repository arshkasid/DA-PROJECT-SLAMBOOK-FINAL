from django import template
# by templates we can make our own tag like crispy form tag 
from social.models import Notification

register = template.Library()

# using a including tag
@register.inclusion_tag('social/show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
	return {'notifications': notifications}