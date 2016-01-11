# encoding:utf8
__author__ = 'brianyang'

import re
from model import Article, Tag, Category, ArticleRedis
from model import Session
from sqlalchemy import func
from util import get_redis_client

redis_client = get_redis_client()


def get_articles(page_num, page_size, category=None, tag=None):
    session = Session()
    if category is not None:
        articles = session.query(Article.id, Article.title, Article.create_time).join(Category).filter(
            Category.name == category).order_by(Article.create_time.desc())[
                   (page_num - 1) * page_size:page_num * page_size]
    elif tag is not None:
        articles = session.query(Article.id, Article.title, Article.create_time).join(Category).filter(
            Article.tags.any(Tag.name == tag)).filter(Article.category is not None).order_by(
            Article.create_time.desc()).all()
    else:
        articles = session.query(Article.id, Article.title, Article.create_time).join(Category).filter(
            Article.category is not None).order_by(Article.create_time.desc())[
                   (page_num - 1) * page_size:page_num * page_size]
    parsed_articled = []
    for article in articles:
        id, title, create_time = article
        #文章对应的标签，暂时禁用
        #tags = session.query(Tag).filter(Article.tags).filter(Article.id == id).all()
        tags = []
        parsed_articled.append({'id': id, 'title': title, 'create_time': create_time, 'tags': tags})
    session.close()
    return parsed_articled


def get_articles_count(category=None, tag=None):
    session = Session()
    if category is not None:
        count = session.query(Article).join(Category).filter(
            Category.name == category).count()
    elif tag is not None:
        count = session.query(Article).filter(Article.tags.any(Tag.name == tag)).count()
    else:
        count = session.query(Article).filter(Article.category != '').count()
    session.close()
    return count


article_detail_expire_time = 3600
article_detail_redis_key = 'article_detail'


def get_article(article_id):
    redis_key = article_detail_redis_key + ':' + article_id
    (art_id, article_title, article_content, article_author, article_create_time, article_tags, article_category_id,
     article_category_name) = redis_client.hmget(
        redis_key, 'id', 'title', 'content', 'author', 'create_time', 'tags', 'category_id', 'category_name')
    if not art_id:
        session = Session()
        article, category = session.query(Article, Category.name).join(Category).filter(
            Article.id == article_id).first()
        article.content = re.sub("\"\"\"", r'＂＂＂', article.content)
        article.title = re.sub("\"\"\"", r'＂＂＂', article.title)
        redis_client.hmset(redis_key, {'id': article.id, 'title': article.title, 'content': article.content,
                                       'author': article.author, 'create_time': article.create_time,
                                       'tags': article.tags, 'category_id': article.category,
                                       'category_name': category})
        redis_client.expire(redis_key, article_detail_expire_time)
        session.close()
    else:
        article = ArticleRedis(art_id, article_title, article_content, article_author, article_create_time,
                               article_tags, article_category_id)
        category = article_category_name
    return article, category


def get_pre_article(article):
    session = Session()
    result = session.query(Article.id, Article.title).filter(Article.category == article.category).filter(
        Article.create_time > article.create_time).order_by(
        Article.create_time).first()
    session.close()
    if result is None:
        return None, None
    article_id, title = result
    return article_id, title


def get_next_article(article):
    session = Session()
    result = session.query(Article.id, Article.title).filter(Article.category == article.category).filter(
        Article.create_time < article.create_time).order_by(
        Article.create_time.desc()).first()
    session.close()
    if result is None:
        return None, None
    article_id, title = result
    return article_id, title


categories_expire_time = 3600
categories_redis_key = "categories_count"


def get_categories():
    categories_str = redis_client.get(categories_redis_key)
    categories_list = eval(categories_str) if categories_str is not None else None
    if not categories_list:
        session = Session()
        categories = session.query(Category.name, func.count(Article).label('count')).filter(
            Article.category == Category.id).group_by(
            Category.name).all()
        redis_client.set(categories_redis_key, categories, categories_expire_time)
        session.close()
    else:
        categories = []
        for item in categories_list:
            name, count = item
            categories.append({'name': name, 'count': count})
    return categories

