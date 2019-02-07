from django.conf.urls import url
from public.views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^users/$', UserListView.as_view(), name='users'),
    url(r'^article/(?P<article_pk>\d+)/(?P<pk>\d+)/$', PageDetailView.as_view(), name='page'),
]
