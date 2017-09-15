# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from app_faq.models.answer import Answer
from app_faq.models.bounty import (Bounty, BountyAward)
from app_faq.models.comment import Comment
from app_faq.models.favorite import Favorite
from app_faq.models.flag import Flag
from app_faq.models.help import Help
from app_faq.models.message import Message
from app_faq.models.question import Question
from app_faq.models.tag import Tag

from app_faq.admin.tag import TagAdmin


admin.site.register(Answer)
admin.site.register(Bounty)
admin.site.register(BountyAward)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Flag)
admin.site.register(Help)
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Tag, TagAdmin)
