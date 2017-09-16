# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import ast
import hashlib
from django import template
from django.utils.module_loading import import_string

try:
    # Python 3
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

register = template.Library()


@register.filter
def splitter(value, sep='.'):
    """
    return splited list.
    :param `value` is value to split.
    :param `sep` is splitter.

    usage:
        {{ value|splitter:"/" }}
    """
    return value.split(sep)


@register.filter
def gravatar(email, size="75"):
    """
    return gravatar url.
    :param `email` is email from user.
    :param `size` is string size of image.

    usage:
        {{ request.user.email|gravatar:"75" }}
    """
    if email is None:
        email = 'fake@email.com'

    gravatar_url = "//www.gravatar.com/avatar/" + \
        hashlib.md5(email.encode('utf-8')).hexdigest() + "?"
    gravatar_url += urlencode({'d': 'retro', 's': str(size)})
    return gravatar_url


@register.filter
def wordsonly(value):
    """
    return string words only.
    :param `value` is value from text or words.

    usage:
        {{ post.description|striptags|truncatewords:"20"|wordsonly }}
    """
    return re.sub(r'[^\w\s]', '', value, flags=re.I | re.M)


@register.filter
def numberize(number):
    """
    return convert number to string, an example:
        - 1000 to 1k
        - 1000000 to 1m, etc.
    :param `number` is number to convert.

    usage:
        {{ post.get_visitors.count|numberize }}
    """
    if type(number) == int:
        if number > 999 and number <= 999999:
            return "{0:.1f}k".format(number / 1000)
        elif number > 999999 and number <= 999999999:
            return "{0:.1f}m".format(number / 1000000)
        elif number > 999999999 and number <= 999999999999:
            return "{0:.1f}b".format(number / 1000000000)
        elif number > 999999999999 and number <= 999999999999999:
            return "{0:.1f}t".format(number / 1000000000000)
        else:
            return "{}".format(number)
    return "{}".format(number)


@register.filter
def has_group(user, mode='single'):
    """
    return group/s object/s from user.
    :param `user` is user object.
    :param `mode` is single/plural mode.

    single:
        {{ request.user|has_group }}

    plural:
        {{ request.user|has_group:"plural" }}
    """
    if mode.lower() == 'plural':
        return user.groups.all()
    return user.groups.first()


@register.filter
def get_tuple_value(tuples, key):
    """
    an example tuples for:
        tuples = (
            ("1", "Afghanistan"),
            ("2", "Albania"),
            ("3", "Algeria")
        )
    :param `tuples` is tuples inside tuple.
    :param `key` is the key from per-single tuple.

    usage:
        {{ tuples|get_tuple_value:"1" }}
    """
    for k, v in tuples:
        if k == key:
            return v
    return key


@register.filter
def markdown_find_images(markdown_text):
    """
    return list of image urls inside `markdown_text`.
    :param `markdown_text` is markdown text to find.

    example markdown text:
        Hello ![title](/path/to/image.png)

    provides for:
        jpeg|jpg|png|gif

    demo:
        https://goo.gl/3LEXom

    usage:
        {{ field_name|markdown_find_images }}

    example:
        {{ post.description|markdown_find_images }}
    """
    # findgex = r"[^(\s]+\.(?:jpeg|jpg|png|gif)(?=\b[+^\)])"
    findgex = r"[^(\s]+\.(?:jpeg|jpg|png|gif)(?=\))"
    return re.findall(findgex, markdown_text)
