# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class RangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(RangeField, self).formfield(**defaults)


class Article(models.Model):
    title = models.CharField(max_length=256, unique=True)

    def __str__(self, ):
        return self.title

    def get_first_page(self, ):
        return self.pages.first()


class Page(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="pages")
    content = models.TextField()
    number = models.PositiveIntegerField()

    def __str__(self, ):
        return "{} page {}".format(self.article.title, self.number)

    def get_next_page(self, ):
        try:
            return Page.objects.get(
                number=(self.number + 1),
                article=self.article
            )
        except:
            return False

    def get_prev_page(self, ):
        try:
            return Page.objects.get(
                number=(self.number - 1),
                article=self.article
            )
        except:
            return False


class Hit(models.Model):
    page = models.ForeignKey("Page", on_delete=models.CASCADE, related_name="hits")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hits")
    count = models.PositiveIntegerField(default=1)
    rating = RangeField(min_value=1, max_value=5, null=True)

    def __str__(self, ):
        return "{} hit page {} {} times".format(self.user.username, self.page.id, self.count)
