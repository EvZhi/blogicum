from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (
    CreateView, DetailView, DeleteView, ListView, UpdateView
)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from blog.constants import PUGINATION_NUMBER
from blog.forms import CommentForm, PostForm
from blog.mixins import (
    OnlyAuthorMixin, PostQuerySetMixin, PostMixin, CommentMixin
)
from blog.models import Category, Post


class IndexView(PostQuerySetMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = PUGINATION_NUMBER

    def get_queryset(self):
        return super().get_queryset().published()


class CategoryPostListView(PostQuerySetMixin, ListView):
    template_name = 'blog/category.html'
    model = Category
    paginate_by = PUGINATION_NUMBER

    def get_object(self):
        return get_object_or_404(
            self.model,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .published()
            .filter(
                category__slug=self.kwargs['category_slug']
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context


class ProfileView(PostQuerySetMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PUGINATION_NUMBER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        self.user_obj = get_object_or_404(
            User, username=self.kwargs['username']
        )
        qs = super().get_queryset().filter(
            author__username=self.user_obj.username
        )
        if (
            self.request.user.is_authenticated
            and self.request.user.username == self.user_obj.username
        ):
            return qs
        return qs.published()


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user.username,))


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = self.get_object(
        ).comment.select_related('author')
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            self.condition |= Q(author_id=self.request.user.id)
        return qs.filter(self.condition)


class PostEditView(LoginRequiredMixin, PostMixin, OnlyAuthorMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect(
                'blog:post_detail',
                self.kwargs.get('post_id')
            )
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(
    LoginRequiredMixin, PostMixin, OnlyAuthorMixin, DeleteView
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(instance=self.object)
        context['form'] = form
        return context
    pass


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    pass


class CommentCreateView(CommentMixin, CreateView):
    pass


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass


class CommentEditView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pass
