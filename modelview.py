__author__ = 'brianyang'

from flask_admin.contrib.sqla import ModelView

from model import Tag, Article


class TagView(ModelView):
    column_filters = ('name',)

    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)


class ArticleView(ModelView):
    column_display_all_relations = ('display_all_relations',
                                    'list_display_all_relations',
                                    True)
    column_list = ('category',)
    can_view_details = True
    column_details_list = ('category',)

    def __init__(self, session, **kwargs):
        super(ArticleView, self).__init__(Article, session, **kwargs)
