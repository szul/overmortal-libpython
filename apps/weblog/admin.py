from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from models import Category, Post
from forms import CategoryForm, PostForm

@login_required
def blog(request, page = 1):
    page = int(page)
    current_page = int(page)
    paginator = Paginator(Post.objects.all().order_by("-date_created"), 75)
    posts = paginator.page(current_page)
    if posts.has_previous():
        previous_page = page - 1
    if posts.has_next():
        next_page = page + 1
    return render_to_response('admin/blog.html', locals())

@login_required
def post(request, post_id = None):
    post = None
    if post_id:
        post = Post.objects.get(id = post_id)
    if request.method == 'POST':
            if post:
                form = PostForm(request.POST, instance = post)
            else:
                form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('overmortal.apps.weblog.admin.blog'))
    else:
        if post:
            form = PostForm(instance = post)
        else:
            form = PostForm()
    return render_to_response('admin/post.html', locals())

@login_required
def delete_post(request, post_id):
    Post.objects.get(id = post_id).delete();
    return HttpResponseRedirect(reverse('overmortal.apps.weblog.admin.blog'))

@login_required
def categories(request):
    categories = Category.objects.all().order_by("name")
    return render_to_response('admin/categories.html', locals())

@login_required
def category(request, category_id = None):
    category = None
    if category_id:
        category = Category.objects.get(id = category_id)
    if request.method == 'POST':
        if category:
            form = CategoryForm(request.POST, instance = category)
        else:
            form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('overmortal.apps.weblog.admin.categories'))
    else:
        if category:
            form = CategoryForm(instance = category)
        else:
            form = CategoryForm()
    return render_to_response('admin/category.html', locals())

@login_required
def delete_category(request, category_id):
    Category.objects.get(id = category_id).delete();
    return HttpResponseRedirect(reverse('overmortal.apps.weblog.admin.categories'))
