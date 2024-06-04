from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView
)
from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.models import Category, Post, Comments
from blog.forms import PostForm, CommentsForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class IndexView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'


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
        return Post.published.filter(author__username=self.kwargs['username'])


class EditProfileView(LoginRequiredMixin, UpdateView):
    fields = ('username', 'first_name', 'last_name', 'email')
    model = User
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))


class PostDeteailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context['post'] = post
        context['form'] = CommentsForm()
        context['comments'] = post.comments.select_related('author')
        return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form = PostForm(instance=post)
        context['form'] = form
        return context


class EditPostView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryPostListView(ListView):
    template_name = 'blog/category.html'
    model = Category
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            self.model,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        posts = (
            self.category
            .posts
            .filter(category__slug=self.kwargs['category_slug'])
        )
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.post_obj.pk})


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    post_obj = None

    def form_valid(self, form):
        self.post_obj = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context

    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        pk = post.pk
        return reverse('blog:post_detail', args=(pk,))


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context

    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        pk = post.pk
        return reverse('blog:post_detail', args=(pk,))
