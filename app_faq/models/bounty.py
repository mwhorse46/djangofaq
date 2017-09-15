# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from app_faq.models.answer import Answer
from app_faq.models.question import Question
from app_faq.models.time import TimeStampedModel


class Bounty(models.Model):
    """
    user create a bounty for the question
    """
    user = models.ForeignKey(
        User, related_name='bounty_user')

    question = models.ForeignKey(
        Question, related_name='bounty_question')

    price = models.PositiveIntegerField(_('Price'))

    is_active = models.BooleanField(
        _('is active bounty?'), default=True)

    start_date = models.DateTimeField(auto_now_add=True)

    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        setup `self.end_date` of bounty for 7 days.
        so the bounty would `is_active=False` after 7 days creation.
        """
        self.end_date = self.start_date + timezone.timedelta(days=7)

        # if timezone.now().date() == self.end_date.date():
        #    self.is_active = False

        super(Bounty, self).save(*args, **kwargs)

    def __str__(self):
        return _('%(user)s bounted a question %(question)s with price %(price)s') % {
            'user': self.user, 'question': self.question, 'price': self.price}

    class Meta:
        verbose_name_plural = _('bounties')
        ordering = ['-start_date']


class BountyAward(TimeStampedModel):
    """
    answer to get a bounty from the bounty.
    """
    bounty = models.ForeignKey(
        Bounty, related_name='bounty_award')

    answer = models.ForeignKey(
        Answer, related_name='bounty_award_for_answer')

    price = models.PositiveIntegerField(_('Price'))

    def __str__(self):
        return _('%(receiver)s awarded a bounty +%(price)s from %(sender)s') % {
            'receiver': self.answer.author, 'price': self.price, 'sender': self.bounty.user}

    class Meta:
        verbose_name_plural = _('bounty awards')
        ordering = ['-created']
