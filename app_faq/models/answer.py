# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from updown.fields import RatingField

from app_faq.models.question import Question
from app_faq.models.time import TimeStampedModel


class AnswerQuerySet(models.QuerySet):

    def approved(self):
        return self.filter(status='approved')

    def duplicated(self):
        return self.filter(status='duplicated')

    def pending(self):
        return self.filter(status='pending')

    def on_hold(self):
        return self.filter(status='on_hold')

    def closed(self):
        return self.filter(status='closed')

    def deleted(self):
        return self.filter(status='deleted')


@python_2_unicode_compatible
class Answer(TimeStampedModel):
    author = models.ForeignKey(
        User, related_name='answer_author')

    question = models.ForeignKey(
        Question, related_name='answer_question')

    STATUS_CHOICES = (
        ('approved', _('Approved')),
        ('duplicated', _('Duplicated')),
        ('pending', _('Pending')),
        ('on_hold', _('On Hold')),
        ('closed', _('Closed')),
        ('deleted', _('Deleted'))
    )
    status = models.CharField(
        _('Status'), max_length=20,
        choices=STATUS_CHOICES, default='approved')

    description = models.TextField(_('Description'))

    rating = RatingField(can_change_vote=True)

    edited = models.BooleanField(
        _('Edited?'), default=False)

    editor = models.ForeignKey(
        User, blank=True, null=True,
        on_delete=models.SET_NULL, related_name='answer_editor')

    objects = AnswerQuerySet.as_manager()

    def __str__(self):
        _title = _('%(author)s comment on %(question)s')
        return _title % {'author': self.author, 'question': self.question}

    class Meta:
        verbose_name_plural = _('answers')
        ordering = ['-created']
