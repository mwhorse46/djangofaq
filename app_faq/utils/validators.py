# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import (RegexValidator, _lazy_re_compile)

# NOT USED YET

slug_re = _lazy_re_compile(r'^[-a-zA-Z0-9_]+\Z')
tag_slug_validators = RegexValidator(
    slug_re,
    # Translators: "letters" means latin letters: a-z and A-Z.
    _("Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens."),
    'invalid'
)
