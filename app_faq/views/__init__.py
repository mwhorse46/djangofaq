# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
to handle a huge import with multiple names.

eg:
    >>> from app_faq.views.answer import AnswerFormView
to:
    >>> from app_faq.views import AnswerFormView
"""

__all__ = [
    'AnswerFormView',

    'CommentFormView', 'CommentQuestionFormView',
    'CommentAnswerFormView', 'CommentsOffsetView',

    'QuestionHomePage', 'QuestionsTagged', 'QuestionRedirectView',
    'QuestionDetail', 'QuestionCreate', 'QuestionSuggestedEditsCreate',
    'QuestionSuggestedEditsReversions',

    'TagListView', 'TagSearchOffset', 'TagSearchJSON',
]

from app_faq.views.answer import *
from app_faq.views.comment import *
from app_faq.views.question import *
from app_faq.views.tag import *
