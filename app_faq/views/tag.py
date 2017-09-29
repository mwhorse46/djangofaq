# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.views.generic import (ListView, DetailView, TemplateView)
from django.db.models.functions import Lower as LowerCase
from django.db.models import (Q, Count)

from app_faq.utils.json import JSONResponseMixin
from app_faq.utils.paginator import GenericPaginator
from app_faq.models.tag import Tag


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'
    paginate_by = settings.TAGS_PER_PAGE
    template_name = 'app_faq/tags.html'

    def get_queryset(self):
        order = self.request.GET.get('order', 'popular')
        tags = self.model.objects.order_by('-created')
        if order == 'popular':
            tags = self.model.objects.annotate(
                total=Count('question_tags')).order_by('-total')
        elif order == 'name':
            tags = self.model.objects.order_by(LowerCase('title').asc())
        elif order == 'new':
            tags = tags
        return tags

    def page_range(self):
        return GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['page_range'] = self.page_range()
        return context


class TagSearchOffset(ListView):
    model = Tag
    context_object_name = 'tags'
    paginate_by = settings.TAGS_PER_PAGE
    template_name = 'app_faq/tags_search_offset.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return self.model.objects.filter(Q(title__startswith=query))


class TagSearchJSON(JSONResponseMixin, TemplateView):
    model = Tag

    def get_queryset(self, query):
        return list(self.model.objects.filter(
            Q(title__startswith=query)).values('title', 'slug', 'id'))

    def get(self, request, *args, **kwargs):
        context = {'success': False, 'results': []}
        query = request.GET.get('q')
        if query is not None and query.strip() != '':
            context.update({
                'success': True,
                'results': self.get_queryset(query)
            })
        return self.render_to_response(context)
