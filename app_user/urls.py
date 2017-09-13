# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from app_user.views import *

urlpatterns = [
    url(r'^users/$', users, name='users'),
    url(r'^users/profile/$', user_profile, name='user_profile'),
]
