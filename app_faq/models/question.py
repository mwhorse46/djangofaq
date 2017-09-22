# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

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

    def _unique_slug(self):
        """
        return unique slug if origin slug is exist.
        eg: `foo-bar` => `foo-bar-1`
        """
        origin_slug = slugify(self.title)
        unique_slug = origin_slug
        numb = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = self._unique_slug()
        else:  # create
            self.slug = self._unique_slug()
        super(Question, self).save(*args, **kwargs)

    def edits_object(self):
        question = self
        qs = QuestionSuggestedEdits.objects.filter(question=question)
        if qs.exists():
            return qs.first()
        return question

    class Meta:
        verbose_name_plural = _('questions')
        ordering = ['-created']


@python_2_unicode_compatible
class QuestionSuggestedEdits(TimeStampedModel):
    question = models.ForeignKey(
        Question, related_name='suggested_edits_question')

    editor = models.ForeignKey(
        User, related_name='suggested_edits_editor')

    title = models.CharField(
        _('Title'), max_length=200)

    slug = models.SlugField(
        _('Slug'), max_length=200, unique=True)

    tags = models.ManyToManyField(
        Tag, related_name='suggested_edits_tags')

    STATUS_CHOICES = (
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('pending', _('Pending'))
    )
    status = models.CharField(
        _('Status'), max_length=20,
        choices=STATUS_CHOICES, default='pending')

    description = models.TextField(_('Description'))

    comment = models.TextField(_('Revision Comment'))
