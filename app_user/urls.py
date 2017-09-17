# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from app_user.views import *

urlpatterns = [
    url(
        r'^users/$',
        UserListView.as_view(),
        name='users'
    ),
    url(
        r'^users/(?P<pk>[\d-]+)/$',
        UserProfileRedirectView.as_view(),
        name='user_profile_redirect'
    ),
    url(
        r'^users/(?P<pk>[\d-]+)/(?P<username>[\w\-]+)/$',
        UserProfile.as_view(),
        name='user_profile'
    ),
    url(
        r'^users/edit/$',
        UserProfileEdit.as_view(),
        name='user_profile_edit'
    ),
]
