# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from martor.widgets import AdminMartorWidget
from app_faq.models.answer import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['description', ]
        widgets = {'description': AdminMartorWidget()}
