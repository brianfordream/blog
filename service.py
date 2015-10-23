__author__ = 'brianyang'

from model import Article, Tag, Category
from model import Session
from sqlalchemy import func


def get_articles(page_num, page_size, category=None, tag=None):
    session = Session()
    if category is not None:
        articles = session.query(Article.id, Article.title, Article.create_time).join(Category).filter(
            Category.name == category).order_by(Article.create_time.desc())[
                   (page_num - 1) * page_size:page_num * page_size]
    elif tag is not None:
        articles = session.query(Article.id, Article.title, Article.create_time).filter(
            Article.tags.any(Tag.name == tag)).order_by(Article.create_time.desc()).all()
    else:
        articles = session.query(Article.id, Article.title, Article.create_time).order_by(Article.create_time.desc())[
                   (page_num - 1) * page_size:page_num * page_size]
    parsed_articled = []
    for article in articles:
        id, title, create_time = article
        tags = session.query(Tag).filter(Article.tags).filter(Article.id == id).all()
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
        count = session.query(Article).count()
    return count


def get_article(article_id):
    session = Session()
    article, category = session.query(Article, Category.name).join(Category).filter(Article.id == article_id).one()
    session.close()
    return article, category


def get_pre_article(article):
    session = Session()
    result = session.query(Article.id, Article.title).filter(Article.category == article.category).filter(
        Article.create_time > article.create_time).order_by(
        Article.create_time).first()
    if result is None:
        return None, None
    article_id, title = result
    return article_id, title


def get_next_article(article):
    session = Session()
    result = session.query(Article.id, Article.title).filter(Article.category == article.category).filter(
        Article.create_time < article.create_time).order_by(
        Article.create_time.desc()).first()
    if result is None:
        return None, None
    article_id, title = result
    return article_id, title


def get_categories():
    session = Session()
    categories = session.query(Category.name, func.count(Article).label('count')).filter(
        Article.category == Category.id).group_by(
        Category.name).all()
    return categories

