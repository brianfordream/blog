# encoding:utf8
__author__ = 'brianyang'
from sqlalchemy import Column, String, Text, Integer, DateTime, Table, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata.clear()
engine = create_engine('mysql+mysqldb://root:199095@localhost/blog', echo=True, convert_unicode=True)
Session = sessionmaker(bind=engine)

article_tag = Table('article_tag', Base.metadata,
                    Column('article_id', Integer, ForeignKey('article.id')),
                    Column('tag_id', Integer, ForeignKey('tag.id')))


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    content = Column(Text)
    author = Column(String(16))
    create_time = Column(DateTime)
    tags = relationship('Tag', secondary=article_tag, backref='article')
    category = Column(Integer, ForeignKey('category.id'))

    def __repr__(self):
        return 'title:%s,author:%s,tags:%s' % (self.title, self.author, self.tags)


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))

    def __repr__(self):
        return 'tag:%s' % (self.name,)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    articles = relationship('Article')


Base.metadata.create_all(engine)