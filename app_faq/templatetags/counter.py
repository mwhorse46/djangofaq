# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from app_faq.models.question import Question
from app_faq.models.answer import Answer

register = template.Library()


@register.filter
def get_total_questions_tagged(tag):
    """
    usage in: `app_faq/tags.html`

    {{ tag|get_total_questions_tagged }}

    return total questions tagged
    and excluded from status='deleted'
    """
    qs = Question.objects.exclude(status='deleted')
    return qs.filter(tags=tag).count()


@register.filter
def get_total_votes(question):
    """
    usage in: `app_faq/question_homepage.html`

    {{ question|get_total_votes }}
    """
    return question.rating_likes


@register.filter
def get_total_answers(question):
    """
    usage in: `app_faq/question_homepage.html`

    {{ question|get_total_answers }}
    """
    return Answer.objects.filter(question=question).count()


@register.filter
def get_total_views(question):
    """
    usage in: `app_faq/question_homepage.html`

    {{ question|get_total_views }}
    """
    return 0
