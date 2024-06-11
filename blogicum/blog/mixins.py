from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostQuerySetMixin:
    def get_queryset(self):
        return (
            Post.post_manager
            .with_related_data()
            .with_comment_count()
        )


class PostMixin(PostQuerySetMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    condition = Q(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['post_id']
        )

    def get_success_url(self):
        slug = self.request.user.username
        return reverse('blog:profile', args=(slug,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_id']])
