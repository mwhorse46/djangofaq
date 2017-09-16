# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.views.generic import (ListView, DetailView)
from django.db.models import Q

from app_faq.utils.paginator import GenericPaginator
from app_faq.models.tag import Tag


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'
    paginate_by = settings.TAGS_PER_PAGE
    template_name = 'app_faq/tags.html'

    def get_queryset(self):
        return self.model.objects.order_by('-created')

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
