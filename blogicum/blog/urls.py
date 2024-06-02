from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),

    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),

    path('category/<slug:category_slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
