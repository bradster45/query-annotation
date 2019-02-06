from django.conf.urls import url
from public.views import *

urlpatterns = [
    url(
        r'^$',
        HomeView.as_view(),
        name='home'
    ),
    url(
        r'^users/$',
        UserListView.as_view(),
        name='users'
    ),
]
