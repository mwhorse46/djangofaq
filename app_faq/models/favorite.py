# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app_faq.models.time import TimeStampedModel
from app_faq.models.content_type import ContentTypeToGetModel


@python_2_unicode_compatible
class Favorite(TimeStampedModel, ContentTypeToGetModel):
    user = models.ForeignKey(
        User, related_name='user_favorite')

    content_type = models.ForeignKey(
        ContentType, related_name='favorites',
        on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField(_('Object id'))

    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '%s' % self.get_related_object()

    class Meta:
        verbose_name = _('Detail Favorite')
        verbose_name_plural = _('Favorites')
        ordering = ['-created']
