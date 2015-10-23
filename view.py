# encoding: utf8
__author__ = 'brianyang'
from flask import Blueprint, render_template
from service import get_articles, get_article, get_categories, get_articles_count, get_next_article, get_pre_article
from util import page_slice

import sys

reload(sys)
sys.setdefaultencoding('utf8')

blog = Blueprint(__file__, 'article')
page_size = 8


@blog.route('/')
def index():
    total = get_articles_count()
    pre, behind = page_slice('/article', total, 1, page_size)
    articles = get_articles(page_num=1, page_size=page_size)
    categories = get_categories()
    return render_template('index.html', articles=articles, categories=categories, pre=pre, behind=behind)


@blog.route('/article/<int:page_num>/')
def article_list(page_num):
    total = get_articles_count()
    pre, behind = page_slice('/article', total, page_num, page_size)
    articles = get_articles(page_num=page_num, page_size=page_size)
    categories = get_categories()
    return render_template('index.html', articles=articles, categories=categories, pre=pre, behind=behind)


@blog.route('/article/detail/<article_id>/')
def article_detail(article_id):
    article, category = get_article(article_id)
    pre_id, pre_title = get_pre_article(article)
    next_id, next_title = get_next_article(article)
    categories = get_categories()
    return render_template('detail.html', article=article, categories=categories,
                           pre_article={'id': pre_id, 'title': pre_title},
                           next_article={'id': next_id, 'title': next_title}, category=category)


@blog.route('/category/<category>/<int:page_num>/')
def category_classify(category, page_num):
    total = get_articles_count(category=category)
    pre, behind = page_slice('/category/{}'.format(category), total, page_num, page_size)
    articles = get_articles(category=category, page_num=page_num, page_size=page_size)
    categories = get_categories()
    return render_template('index.html', articles=articles, categories=categories, pre=pre, behind=behind)


@blog.route('/tag/<tag>/<int:page_num>/')
def tag_classify(tag, page_num):
    total = get_articles_count(tag=tag)
    pre, behind = page_slice('/tag/{}'.format(tag), total, page_num, page_size)
    articles = get_articles(tag=tag, page_num=page_num, page_size=page_size)
    categories = get_categories()
    return render_template('index.html', articles=articles, categories=categories, pre=pre, behind=behind)
