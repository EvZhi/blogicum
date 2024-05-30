from django.db.models.functions import Now
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render
)

from blog.models import Category, Post

LIMIT_POSTS = 5
POST_BASE = Post.objects.select_related(
    'category',
    'location',
    'author'
).filter(
    pub_date__lte=Now(),
    is_published=True,
    category__is_published=True
)


def index(request):
    template_name = 'blog/index.html'
    post_list = POST_BASE.all()[:LIMIT_POSTS]
    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(POST_BASE, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_list_or_404(
        POST_BASE,
        category__slug=category_slug
    )
    context = {
        'post_list': post_list,
        'category': category
    }

    return render(request, template_name, context)
