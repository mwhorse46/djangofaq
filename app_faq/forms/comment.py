# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from app_faq.models.comment import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', ]
