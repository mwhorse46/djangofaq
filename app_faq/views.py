# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def question_homepage(request):
    template_name = 'app_faq/question_homepage.html'
    return render(request, template_name, {})


def question_detail(request):
    template_name = 'app_faq/question_detail.html'
    return render(request, template_name, {})


def tags(request):
    template_name = 'app_faq/tags.html'
    return render(request, template_name, {})
