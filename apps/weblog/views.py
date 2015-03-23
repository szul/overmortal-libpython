from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.comments.views.comments import post_comment
from django.conf import settings
from models import *

def tag(request, tag, page=1):
    categories = Category.objects.all().order_by('name')
    page = int(page)
    current_page = int(page)
    paginator = Paginator(Post.objects.filter(tags__contains = tag).order_by("-date_created"), 50)
    posts = paginator.page(current_page)
    if posts.has_previous():
        previous_page = page - 1
    if posts.has_next():
        next_page = page + 1
    header_title = "Blog Posts Tagged with " + tag
    return render_to_response('blog.html', locals())

def blog(request, page=1, category_slug=None):
    weblog_title = settings.WEBLOG_TITLE
    categories = Category.objects.all().order_by('name')
    page = int(page)
    current_page = int(page)
    if category_slug is None:
        paginator = Paginator(Post.objects.filter(is_draft = False).order_by("-date_created"), 25)
    else:
        category_name = Category.objects.filter(slug = category_slug)[0].name
        paginator = Paginator(Post.objects.filter(is_draft = False, category__slug = category_slug).order_by("-date_created"), 25)
    posts = paginator.page(current_page)
    if posts.has_previous():
        previous_page = page - 1
    if posts.has_next():
        next_page = page + 1
    return render_to_response('blog.html', locals())

def override_post_comment(request):
    response = post_comment(request)
    if(response.content.find('Preview your Comments') == -1):
        if request.POST['object_pk']:
            post = Post.objects.get(id=request.POST['object_pk'])
            if post:
                return HttpResponseRedirect(post.get_absolute_url())
    return response

def post(request, post_id):
    post = Post.objects.get(id = post_id)
    categories = Category.objects.all().order_by('name')
    return render_to_response('post.html', locals())

def rss(request):
    return render_to_response('rss.html', locals())
