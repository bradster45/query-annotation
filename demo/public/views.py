# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.views.generic import ListView, DetailView
from django.db.models import Avg, Sum, Case, When, Count, IntegerField

from public.models import *

class HomeView(ListView):
    model = Article
    paginate_by = 15

    def get_queryset(self):
        order = self.request.GET.get('order', '-views')
        self.order = order
        analytics = Article.objects.all().annotate(
            views=Sum(
                Case(
                    When(
                        pages__hits__count__gte=0,
                        then='pages__hits__count'
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).annotate(
            unique_views=Count('pages__hits')
        ).annotate(
            average_rating=Avg('pages__hits__rating')
        ).order_by(
            order
        )
        return analytics


class UserListView(ListView):
    model = User
    template_name = 'public/user_list.html'
    paginate_by = 15

    def get_queryset(self):
        order = self.request.GET.get('order', '-views')
        self.order = order
        analytics = User.objects.filter(
            is_staff=False
        ).annotate(
            views=Sum(
                Case(
                    When(
                        hits__count__gte=0,
                        then='hits__count'
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).annotate(
            unique_views=Count('hits')
        ).annotate(
            average_rating=Avg('hits__rating')
        ).order_by(
            order
        )
        return analytics


class PageDetailView(DetailView):
    model = Page

    # increase page hit
    def get_object(self, ):
        pk = self.kwargs.get(self.pk_url_kwarg)
        page = Page.objects.get(pk=pk)
        hit, hit_created = Hit.objects.get_or_create(
            page=page,
            user=self.request.user,
            defaults={
                'rating': random.randint(1, 5)
            }
        )
        if not hit_created:
            hit.count += 1
            hit.save()
        return page
