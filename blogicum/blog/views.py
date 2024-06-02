from django.contrib.auth.models import User
from django.db.models.functions import Now
from django.shortcuts import redirect
from django.views.generic import  CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render,
)
from django.urls import reverse_lazy, reverse

from blog.models import Category, Post
from blog.forms import PostForm

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


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        return POST_BASE.filter(author__username=self.kwargs['username'])


class EditProfileView(UpdateView):
    fields = ('username', 'first_name', 'last_name', 'email')
    model = User
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'


class DeletePostView(DeleteView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(instance=instance)
        context['form'] = form
        return context


class IndexView(ListView):
    model = Post

    paginate_by = 10
    template_name = 'blog/index.html'


# def index(request):
#     template_name = 'blog/index.html'
#     post_list = POST_BASE.all()[:LIMIT_POSTS]
#     context = {
#         'page_obj': post_list,
#     }
#     return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(POST_BASE, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, template_name, context)


class CategoryPostListView(ListView):
    template_name = 'blog/category.html'
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        post_list = get_list_or_404(
            POST_BASE,
            category__slug=self.kwargs['category_slug']
        )
        context = {
            'page_obj': post_list,
            'category': category
        }
        return context

# def category_posts(request, category_slug):
#     template_name = 'blog/category.html'
#     category = get_object_or_404(
#         Category,
#         slug=category_slug,
#         is_published=True
#     )
#     post_list = get_list_or_404(
#         POST_BASE,
#         category__slug=category_slug
#     )
#     context = {
#         'page_obj': post_list,
#         'category': category
#     }

    # return render(request, template_name, context)
