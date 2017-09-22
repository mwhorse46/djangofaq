from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

# This problem because we found error encoding,
# as docs says, django has special `DjangoJSONEncoder`
# https://docs.djangoproject.com/en/1.10/topics/serialization/#serialization-formats-json
# and this answer: http://stackoverflow.com/a/31746279/6396981


class LazyEncoder(DjangoJSONEncoder):
    """
    used in: app_forum/views/uploader.py
    """

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
