# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

# from draceditor.models import DraceditorField
from updown.fields import RatingField
from app_faq.models.tag import Tag
from app_faq.models.time import TimeStampedModel


class QuestionQuerySet(models.QuerySet):

    def published(self):
        return self.exclude(status='deleted')

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

    def edited(self):
        return self.filter(edited=True)

    def unedited(self):
        return self.filter(edited=False)


@python_2_unicode_compatible
class Question(TimeStampedModel):
    author = models.ForeignKey(
        User, related_name='question_author')

    title = models.CharField(
        _('Title'), max_length=200)

    slug = models.SlugField(
        _('Slug'), max_length=200, unique=True)

    tags = models.ManyToManyField(
        Tag, related_name='tags')

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
        on_delete=models.SET_NULL, related_name='question_editor')

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('questions')
        ordering = ['-created']
