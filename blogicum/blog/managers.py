from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def with_related_data(self):
        return self.select_related(
            'category',
            'location',
            'author'
        )

    def with_comment_count(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def published(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
