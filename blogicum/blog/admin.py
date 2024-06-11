from django.contrib import admin
from django.utils.html import mark_safe

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'image_post',
        'pub_date',
        'author',
        'location',
        'category',
    )
    list_display_links = (
        'title',
        'image_post',
        'location',
        'category',
    )

    fieldsets = (
        (None, {
            'fields': (
                'is_published',
                'title',
                'text',
                'pub_date',
                'author',
            )
        }),
        ('Локация и категория', {
            'fields': (
                'category',
                'location',
            )
        }),
        ('Изображение', {
            'fields': (
                'image',
                'image_post',
            )
        }),
    )

    list_per_page = 10

    readonly_fields = ('image_post',)

    list_editable = (
        'is_published',
    )
    list_filter = (
        'category',
        'location',
        'author',

    )
    search_fields = ('title',)

    @admin.display(description='Превью')
    def image_post(self, post: Post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' height=75>")
        return "Без изображения"


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'description',
        'slug',
    )
    list_editable = (
        'is_published',
        'slug',
    )
    inlines = (
        PostInline,
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    inlines = (
        PostInline,
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'post',
        'is_published',
    )
    list_editable = (
        'is_published',
    )

    list_display_links = (
        'author',
        'post',
    )
