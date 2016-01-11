__author__ = 'brianyang'

from flask_admin.contrib.sqla import ModelView
from model import Tag, Article


class TagView(ModelView):
    column_filters = ('name',)

    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)


class ArticleView(ModelView):
    edit_template = 'edit.html'
    create_template = 'create.html'
    page_size = 8
    column_default_sort = ('create_time', True)

    column_filters = ('category', 'tags')
    column_display_all_relations = ('display_all_relations',
                                    'list_display_all_relations',
                                    True)
    column_list = ('title', 'create_time', 'category')

    def __init__(self, session, **kwargs):
        super(ArticleView, self).__init__(Article, session, **kwargs)


