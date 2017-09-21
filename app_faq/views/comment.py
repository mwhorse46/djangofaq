# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from app_faq.models.comment import Comment
from app_faq.forms.comment import CommentForm


class CommentFormView(FormView):
    form_class = CommentForm
    #success_url = ''

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.sender = self.request.user
        initial.receiver = ''
        initial.save()
        messages.success(self.request, _(''))
