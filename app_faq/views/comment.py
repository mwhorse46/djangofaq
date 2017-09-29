# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (ListView, DetailView, FormView)
from django.http import JsonResponse

from app_faq.models.answer import Answer
from app_faq.models.question import Question
from app_faq.models.comment import Comment
from app_faq.forms.comment import CommentForm


class CommentFormView(LoginRequiredMixin, FormView):
    template_name = 'app_faq/comment_create.html'
    form_class = CommentForm
    model_target = None

    def get_object(self):
        return get_object_or_404(self.model_target, pk=self.kwargs['pk'])

    def form_valid(self, form):
        if self.model_target is None:
            return JsonResponse({'status': False})

        model_name = self.model_target._meta.model_name
        content_type = ContentType.objects.get(model=model_name)

        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.content_type = content_type
        initial.object_id = self.get_object().pk
        initial.save()
        form.save()

        context = {
            'status': True,
            'author': self.request.user,
            'comment': initial.comment,
            'created': initial.created,
            'edited': initial.edited,
            'id': initial.id
        }
        # id="question-comment-{{ question.id }}"
        # id="answer-comment-{{ question.id }}"
        return JsonResponse(context)


class CommentQuestionFormView(CommentFormView):
    model_target = Question


class CommentAnswerFormView(CommentFormView):
    model_target = Answer


class CommentsOffsetView(DetailView):
    template_name = 'app_faq/comments_offset.html'

    def get_object(self):
        model_instance = None
        model_name = self.kwargs['model_name']
        object_id = self.kwargs['object_id']
        if model_name == 'question':
            model_instance = get_object_or_404(Question, pk=object_id)
        elif model_name == 'answer':
            model_instance = get_object_or_404(Answer, pk=object_id)
        return model_instance

    def get_comments_offset(self):
        if self.get_object():
            return self.get_object().get_comments_offset()
        return None

    def get_context_data(self, **kwargs):
        context = super(CommentsOffsetView, self).get_context_data(**kwargs)
        context['comments_offset'] = self.get_comments_offset()
        context['object'] = self.get_object()
        return context
