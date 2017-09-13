# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from updown.fields import RatingField
from app_faq.models.time import TimeStampedModel
from app_faq.models.content_type import ContentTypeToGetModel


@python_2_unicode_compatible
class Message(TimeStampedModel, ContentTypeToGetModel):
    sender = models.ForeignKey(
        User, related_name='message_sender')

    receiver = models.ForeignKey(
        User, related_name='message_receiver')

    content_type = models.ForeignKey(
        ContentType, related_name='messages',
        on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField(_('Object id'))

    content_object = GenericForeignKey('content_type', 'object_id')

    read = models.BooleanField(
        _('is read?'), default=False)

    def __str__(self):
        return '%s' % self.get_related_object()

    class Meta:
        verbose_name = _('Detail Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created']
