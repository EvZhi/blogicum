from django.contrib.auth import get_user_model
from django.db import models

from core.models import IsPublishedAndCreatedAtModel

MAX_LENGHT_CHAR = 256

User = get_user_model()


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
        verbose_name='Автор публикации',
        related_name='posts_author'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts_location'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts_category'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', 'title')

    def __str__(self):
        return self.title


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
