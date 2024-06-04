from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.db.models.functions import Now
from django.urls import reverse
from core.models import IsPublishedAndCreatedAtModel

MAX_LENGHT_CHAR = 256

User = get_user_model()


class PostQuerySet(models.QuerySet):

    def with_related_data(self):
        return self.select_related(
            'category',
            'location',
            'author'
        )

    def with_coment_count(self):
        return self.annotate(
            coment_count=Count('comments')
        ).order_by('-pub_date')

    def published(self):
        return self.filter(
            pub_date__lte=Now(),
            is_published=True,
            category__is_published=True
        )


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .with_coment_count()
            .with_related_data()
            .published()
        )


class Post(IsPublishedAndCreatedAtModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGHT_CHAR)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать'
        ' отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(verbose_name='Картинка у публикации', blank=True)

    published = PublishedPostManager()

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.pk,))


class Category(IsPublishedAndCreatedAtModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGHT_CHAR)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(IsPublishedAndCreatedAtModel):
    name = models.CharField('Название места', max_length=MAX_LENGHT_CHAR)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comments(IsPublishedAndCreatedAtModel):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост'
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = ' Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:30]
