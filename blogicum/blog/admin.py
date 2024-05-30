from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
        'category'
    )
    list_filter = (
        'category',
        'location',
        'author'

    )
    search_fields = ('title',)


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'description',
        'slug'
    )
    list_editable = (
        'is_published',
    )
    inlines = (
        PostInline,
    )


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


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
