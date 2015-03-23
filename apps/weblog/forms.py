from django.forms import ModelForm
from models import Category, Post

class CategoryForm(ModelForm):
    class Meta:
        model = Category

class PostForm(ModelForm):
    class Meta:
        model = Post
