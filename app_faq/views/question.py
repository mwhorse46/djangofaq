# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import (get_object_or_404, redirect)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, FormView)
from django.views.generic.base import RedirectView

from app_faq.utils.paginator import GenericPaginator
from app_faq.models.question import Question
from app_faq.models.tag import Tag
from app_faq.forms.answer import AnswerForm
from app_faq.forms.question import QuestionForm


class QuestionHomePage(ListView):
    model = Question
    context_object_name = 'questions'
    paginate_by = settings.QUESTIONS_PER_PAGE
    template_name = 'app_faq/question_homepage.html'

    def get_queryset(self):
        return self.model.objects.published().order_by('-created')

    def page_range(self):
        return GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()

    def get_context_data(self, **kwargs):
        context = super(QuestionHomePage, self).get_context_data(**kwargs)
        context['total_questions'] = self.get_queryset().count()
        context['page_range'] = self.page_range()
        return context


class QuestionRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        return reverse('question_detail', kwargs={'pk': question.pk, 'slug': question.slug})


class QuestionDetail(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'app_faq/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['answer_form'] = AnswerForm
        return context


class QuestionCreate(LoginRequiredMixin, FormView):
    template_name = 'app_faq/question_create.html'
    form_class = QuestionForm

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.author = self.request.user
        print(self.request.POST.get('tags'))
        # initial.tags = Tag
        # initial.save_m2m()
        messages.success(self.request, _('Question successfully created!'))
        # return redirect(reverse('question_redirect', kwargs={'pk': initial.pk}))
