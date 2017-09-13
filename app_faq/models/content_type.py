# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ContentTypeToGetModel(object):

    """
    requires fields:
        - content_type: FK(ContentType)
        - object_id: PositiveIntegerField()
    """

    def get_related_object(self):
        """
        return the related object of content_type.
        eg: <Question: Holisticly grow synergistic best practices>
        """
        # This should return an error: MultipleObjectsReturned
        # return self.content_type.get_object_for_this_type()
        # So, i handle it with this one:
        model_class = self.content_type.model_class()
        return model_class.objects.get(id=self.object_id)

    @property
    def _model_name(self):
        """
        return lowercase of model name.
        eg: `question`, `answer`
        """
        return self.get_related_object()._meta.model_name
