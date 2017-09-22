# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import (get_object_or_404, redirect)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from app_faq.models.question import Question
from app_faq.forms.answer import AnswerForm


class AnswerFormView(LoginRequiredMixin, FormView):
    template_name = 'app_faq/answer_create.html'
    http_method_names = [u'post', ]
    form_class = AnswerForm

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.question = question
        initial.save()
        messages.success(self.request, _('Your answer successfully created!'))
        return redirect(reverse('question_redirect', kwargs={'pk': question.pk}))
