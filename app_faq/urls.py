# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from app_faq.views.question import *
from app_faq.views.answer import *
from app_faq.views.tag import *

urlpatterns = [
    url(
        r'^$',
        QuestionHomePage.as_view(),
        name='question_homepage'
    ),
    url(
        r'^question/(?P<pk>[\d-]+)/$',
        QuestionRedirectView.as_view(),
        name='question_redirect'
    ),
    url(
        r'^question/(?P<pk>[\d-]+)/(?P<slug>[\w\-]+)/$',
        QuestionDetail.as_view(),
        name='question_detail'
    ),
    url(
        r'^question/create/$',
        QuestionCreate.as_view(),
        name='question_create'
    ),
    url(
        r'^question/edit/(?P<pk>[\d-]+)/$',
        QuestionEdit.as_view(),
        name='question_edit'
    ),
    url(
        r'^question/reversions/(?P<pk>[\d-]+)/$',
        QuestionReversions.as_view(),
        name='question_reversions'
    ),
    url(
        r'^answer/(?P<question_id>[\d-]+)/create/$',
        AnswerFormView.as_view(),
        name='answer_create'
    ),
    url(
        r'^tags/$',
        TagListView.as_view(),
        name='tags'
    ),
    url(
        r'^tags/search/offset/$',
        TagSearchOffset.as_view(),
        name='tags_search_offset'
    ),
    url(
        r'^tags/search/json/$',
        TagSearchJSON.as_view(),
        name='tags_search_json'
    ),
]
