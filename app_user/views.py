# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, FormView, UpdateView)
from django.views.generic.base import RedirectView
from django.contrib.auth.models import User

from app_faq.utils.paginator import GenericPaginator
from app_user.models import Profile
from app_user.forms import ProfileForm


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    paginate_by = settings.USERS_PER_PAGE
    template_name = 'app_user/users.html'

    def get_queryset(self):
        return self.model.objects.exclude(
            is_active=False).order_by('-date_joined')

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


class UserProfileRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        return reverse('user_profile', kwargs={'pk': user.pk,
                                               'username': user.username})


class UserProfile(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'app_user/user_profile.html'

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'],
                                 username=self.kwargs['username'])
        profile, truefalse = Profile.objects.get_or_create(user=user)
        return profile


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'app_user/user_profile_edit.html'

    def get_success_url(self):
        return reverse('user_profile_edit',
                       kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        profile, truefalse = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        messages.success(self.request, _('Profile updated!'))
        return super(UserProfileEdit, self).form_valid(form)

    def get_initial(self):
        initial = super(UserProfileEdit, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial
