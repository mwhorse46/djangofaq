# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def users(request):
    template_name = 'app_user/users.html'
    return render(request, template_name, {})


def user_profile(request):
    template_name = 'app_user/user_profile.html'
    return render(request, template_name, {})
