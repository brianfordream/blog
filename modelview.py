__author__ = 'brianyang'

from flask_admin.contrib.sqla import ModelView

from model import Tag


class TagView(ModelView):
    column_filters = ('name',)

    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)