from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'blog'
POSTS_URL = 'posts/<int:post_id>'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path(f'{POSTS_URL}/', views.PostDetailView.as_view(), name='post_detail'),
    path(f'{POSTS_URL}/edit/', views.EditPostView.as_view(), name='edit_post'),
    path(f'{POSTS_URL}/delete/', views.DeletePostView.as_view(), name='delete_post'),


    path(f'{POSTS_URL}/comment', views.CommentCreateView.as_view(), name='add_comment'),
    path(f'{POSTS_URL}/edit_comment/<int:comment_id>/', views.EditCommentView.as_view(), name='edit_comment'),
    path(f'{POSTS_URL}/delete_comment/<int:comment_id>/', views.DeleteCommentView.as_view(),name='delete_comment'),


    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),

    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),

    path('category/<slug:category_slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
