# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from public.models import *

admin.site.register(Article)
admin.site.register(Page)
admin.site.register(Hit)
