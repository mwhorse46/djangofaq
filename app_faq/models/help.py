# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app_faq.models.time import TimeStampedModel


@python_2_unicode_compatible
class Help(TimeStampedModel):
    creator = models.ForeignKey(
        User, related_name='help_creator')

    parent = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='child')

    title = models.CharField(
        _('Title'), max_length=200)

    description = models.TextField(_('Description'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Detail Help')
        verbose_name_plural = _('Helps')
        ordering = ['-created']
