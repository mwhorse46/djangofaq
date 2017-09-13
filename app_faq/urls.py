# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from app_faq.views import *

urlpatterns = [
    url(r'^$', question_homepage, name='question_homepage'),
    url(r'^d/$', question_detail, name='question_detail'),
    url(r'^tags/$', tags, name='tags'),
]
