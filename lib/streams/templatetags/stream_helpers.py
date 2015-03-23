from django import template
from models import Stream

register = template.Library()

@register.inclusion_tag('stream.html')
def get_stream(parser, token):
    items = Stream.objects.all().reverse()
    return { 'items':items }
