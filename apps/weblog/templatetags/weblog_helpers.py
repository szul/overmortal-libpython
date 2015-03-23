from django import template
from tagging.models import Tag
from models import Post

register = template.Library()

@register.filter
def check_font(value):
    if value is None or value == '':
        return '4'
    else:
        return value

@register.tag
def tag_cloud(parser, token):
    return TagCloudObject()

class TagCloudObject(template.Node):
    def render(self, context):
        context['tag_cloud_items'] = Tag.objects.cloud_for_model(Post)
        return ''
