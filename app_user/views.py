# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def users(request):
    template_name = 'app_user/users.html'
    return render(request, template_name, {})


def user_profile(request):
    template_name = 'app_user/user_profile.html'
    return render(request, template_name, {})


from django.conf import settings
from django.views.generic import (ListView, DetailView)

from django.contrib.auth.models import User
from app_faq.utils.paginator import GenericPaginator


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    paginate_by = settings.USERS_PER_PAGE
    template_name = 'app_user/users.html'

    def get_queryset(self):
        return self.model.objects.exclude(is_active=False)

    def page_range(self):
        return GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['page_range'] = self.page_range()
        return context
