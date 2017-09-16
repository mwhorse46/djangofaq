# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from app_faq.models.question import Question

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
