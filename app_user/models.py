# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.ForeignKey(
        User, related_name='profile_user')

    location = models.CharField(
        _('Location'), max_length=200, null=True, blank=True)

    about_me = models.TextField(
        _('About Me'), null=True, blank=True)

    website = models.URLField(
        _('Website'), null=True, blank=True)

    twitter = models.URLField(
        _('Twitter'), null=True, blank=True)

    linkedin = models.URLField(
        _('Linkedin'), null=True, blank=True)

    github = models.URLField(
        _('Github'), null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Detail User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['-user__date_joined']
