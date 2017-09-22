# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin


class FlagAdmin(CompareVersionAdmin):
    #list_display = ['title', 'creator']
    pass
