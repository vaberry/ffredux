from django import template
from app.models import Notification,Owner

register = template.Library()

@register.inclusion_tag('app/show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')
	return {'notifications': notifications}

@register.inclusion_tag('app/get_owners.html', takes_context=True)
def get_owners(context):
	request_user = context['request'].user
	owners = Owner.objects.all().order_by('teamname')
	return {'owners': owners}