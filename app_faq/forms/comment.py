# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from app_faq.models.comment import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', ]
        placeholder = _('Use comments to ask for more information '
                        'or suggest improvements. Avoid answering questions in comments.')
        widgets = {'comment': forms.Textarea(attrs={'placeholder': placeholder})}
