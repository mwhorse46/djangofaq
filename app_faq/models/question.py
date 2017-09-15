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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('questions')
        ordering = ['-created']
