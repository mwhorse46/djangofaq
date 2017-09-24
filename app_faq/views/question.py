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

from django.utils.encoding import force_text
from django.template.loader import render_to_string
# from reversion.models import Version
from reversion.views import RevisionMixin
from reversion_compare.views import HistoryCompareDetailView
from reversion import set_comment as reversion_set_comment

from app_faq.utils.revision import html_diff_custom

from app_faq.utils.paginator import GenericPaginator
from app_faq.models.question import Question, QuestionSuggestedEdits
from app_faq.models.tag import Tag
from app_faq.models.answer import Answer
from app_faq.forms.answer import AnswerForm
from app_faq.forms.question import QuestionForm, QuestionSuggestedEditsForm


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

    def get_answers(self):
        order = self.request.GET.get('order', 'active')
        answers = Answer.objects.approved().filter(question=self.get_object())
        if order == 'active':
            answers = answers.order_by('-modified')
        elif order == 'oldest':
            answers = answers.order_by('created')
        elif order == 'votes':
            answers = answers.order_by('rating_likes')
        return answers

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['answer_form'] = AnswerForm
        context['answers_question'] = self.get_answers()
        return context


class QuestionCreate(LoginRequiredMixin, FormView):
    template_name = 'app_faq/question_create.html'
    form_class = QuestionForm

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.author = self.request.user
        initial.save()
        form.save_m2m()
        messages.success(self.request, _('Question successfully created!'))
        return redirect(reverse('question_redirect', kwargs={'pk': initial.pk}))


class QuestionEdit(LoginRequiredMixin, RevisionMixin, FormView):
    template_name = 'app_faq/question_edit.html'
    form_class = QuestionForm
    model = Question

    def post(self, request, **kwargs):
        comment = request.POST.get('comment', '')
        reversion_set_comment(comment)
        return super(QuestionEdit, self).post(request, **kwargs)

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs['pk'])

    def get_form(self):
        return self.form_class(instance=self.get_object(), **self.get_form_kwargs())

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.editor = self.request.user
        initial.edited = True
        initial.save()
        form.save_m2m()
        messages.info(self.request, _('Question successfully updated!'))
        return redirect(reverse('question_redirect', kwargs={'pk': initial.pk}))

    def get_context_data(self, **kwargs):
        context = super(QuestionEdit, self).get_context_data(**kwargs)
        context['question'] = self.get_object()
        return context


class QuestionSuggestedEditsCreate(LoginRequiredMixin, RevisionMixin, FormView):
    template_name = 'app_faq/question_suggested_edits_create.html'
    form_class = QuestionSuggestedEditsForm
    model = QuestionSuggestedEdits

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs['pk'])

    def form_valid(self, form):
        initial = form.save(commit=False)
        initial.question = self.get_object()
        initial.editor = self.request.user
        initial.save()
        form.save_m2m()

        # updating the last editor
        question = self.get_object()
        question.editor = self.request.user
        question.edited = True
        question.save()

        messages.success(self.request, _('Edit suggestion successfully created!'))
        return redirect(reverse('question_redirect', kwargs={'pk': self.get_object().pk}))

    def get_initial(self):
        initial = super(QuestionSuggestedEditsCreate, self).get_initial()
        for field, _cls in self.form_class.base_fields.items():
            if field == 'tags':
                value = self.get_object().tags.all()
            elif field == 'comment':
                value = ''
            else:
                value = getattr(self.get_object(), field)
            initial.update({field: value})
        return initial

    def get_context_data(self, **kwargs):
        context = super(QuestionSuggestedEditsCreate, self).get_context_data(**kwargs)
        context['question'] = self.get_object()
        return context


"""
class QuestionReversions(ListView):
    template_name = 'app_faq/question_revisions.html'
    context_object_name = 'reversions'
    model = Version

    def get_question(self):
        return get_object_or_404(Question, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.model.objects.get_for_object(self.get_question())

    def get_context_data(self, **kwargs):
        context = super(QuestionReversions, self).get_context_data(**kwargs)
        context['question'] = self.get_question()
        return context
"""


class QuestionReversions(HistoryCompareDetailView):
    template_name = 'app_faq/question_revisions_old.html'
    context_object_name = 'question'
    model = Question
    compare_exclude = ('modified', 'author')

    """
    def fallback_compare(self, obj_compare):
        value1, value2 = obj_compare.to_string()
        html = html_diff_custom(value1, value2)
        return html

    def generic_add_remove(self, raw_value1, raw_value2, value1, value2):
        if raw_value1 is None:
            context = {"value": value2}
            return render_to_string("reversion-compare/compare_generic_add.html", context)
        elif raw_value2 is None:
            context = {"value": value1}
            return render_to_string("reversion-compare/compare_generic_remove.html", context)
        else:
            html = html_diff_custom(value1, value2)
            return html

    def compare_ForeignKey(self, obj_compare):
        related1, related2 = obj_compare.get_related()
        value1, value2 = force_text(related1), force_text(related2)
        return self.generic_add_remove(related1, related2, value1, value2)
    """

    def compare_ManyToOneRel(self, obj_compare):
        change_info = obj_compare.get_m2o_change_info()
        context = {'change_info': change_info}
        return render_to_string('reversion-compare/question/compare_generic_many_to_many.html', context)

    def compare_ManyToManyField(self, obj_compare):
        change_info = obj_compare.get_m2m_change_info()
        context = {'change_info': change_info}
        return render_to_string('reversion-compare/question/compare_generic_many_to_many.html', context)


class QuestionSuggestedEditsReversions(HistoryCompareDetailView):
    template_name = 'app_faq/question_revisions.html'
    context_object_name = 'question'
    model = QuestionSuggestedEdits
    compare_exclude = ('created', 'modified', 'author')

    def get_object(self):
        return get_object_or_404(self.model, question__pk=self.kwargs['pk'])

    def compare_ManyToOneRel(self, obj_compare):
        change_info = obj_compare.get_m2o_change_info()
        context = {'change_info': change_info}
        return render_to_string('reversion-compare/question/compare_generic_many_to_many.html', context)

    def compare_ManyToManyField(self, obj_compare):
        change_info = obj_compare.get_m2m_change_info()
        context = {'change_info': change_info}
        return render_to_string('reversion-compare/question/compare_generic_many_to_many.html', context)
