# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app_faq.models.time import TimeStampedModel
from app_faq.models.content_type import ContentTypeToGetModel


@python_2_unicode_compatible
class Flag(TimeStampedModel, ContentTypeToGetModel):
    creator = models.ForeignKey(
        User, related_name='flag_creator')

    content_type = models.ForeignKey(
        ContentType, related_name='flags',
        on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField(_('Object id'))

    content_object = GenericForeignKey('content_type', 'object_id')

    FLAG_CHOICES = (
        ('spam', _('as spam')),
        ('rude', _('as rude or abusive')),
        ('duplicated', _('as duplicate')),
        ('low-quality', _('as very low quality')),
        ('protected', _('as protected')),
        ('normal', _('as normal'))
    )
    status = models.CharField(
        _('Status'), max_length=20,
        choices=FLAG_CHOICES, default='normal')

    def __str__(self):
        title = _('%(creator)s flagged %(status)s to %(model)s:%(id)s')
        return title % {'creator': self.creator.username, 'status': self.status,
                        'model': self._model_name, 'id': self.object_id}

    class Meta:
        verbose_name = _('Detail Flag')
        verbose_name_plural = _('Flags')
        ordering = ['-created']
