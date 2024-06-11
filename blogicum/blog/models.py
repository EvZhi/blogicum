from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blog.constants import MAX_LENGHT_CHAR, STR_LENGTH
from blog.managers import PostQuerySet
from core.models import IsPublishedAndCreatedAtModel


User = get_user_model()


class Category(IsPublishedAndCreatedAtModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGHT_CHAR)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:STR_LENGTH]


class Location(IsPublishedAndCreatedAtModel):
    name = models.CharField('Название места', max_length=MAX_LENGHT_CHAR)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:STR_LENGTH]


class Post(IsPublishedAndCreatedAtModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGHT_CHAR)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Картинка у публикации',
        upload_to='posts_images',
        blank=True
    )

    post_manager = PostQuerySet.as_manager()
    objects = models.Manager()

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:STR_LENGTH]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.pk,))


class Comment(IsPublishedAndCreatedAtModel):

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
        return (
            f'Комментарий автора {self.author} к посту "{self.post}",'
            f' текст: {self.text[:STR_LENGTH]}...'
        )
