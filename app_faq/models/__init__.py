# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
to handle a huge import with multiple names.

eg:
    >>> from app_faq.models.answer import Answer
to:
    >>> from app_faq.models import Answer
"""

__all__ = [
    'AnswerQuerySet', 'Answer', 'AnswerSuggestedEdits',
    'Bounty', 'BountyAward', 'Comment', 'ContentTypeToGetModel',
    'Favorite', 'Flag', 'Help', 'Message', 'QuestionQuerySet',
    'Question', 'QuestionSuggestedEdits', 'Tag', 'TimeStampedModel'
]

from app_faq.models.answer import *
from app_faq.models.bounty import *
from app_faq.models.comment import *
from app_faq.models.content_type import *
from app_faq.models.favorite import *
from app_faq.models.flag import *
from app_faq.models.help import *
from app_faq.models.message import *
from app_faq.models.question import *
from app_faq.models.tag import *
from app_faq.models.time import *
