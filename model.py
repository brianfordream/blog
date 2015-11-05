# encoding:utf8
__author__ = 'brianyang'
from sqlalchemy import Column, String, Text, Integer, DateTime, Table, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
Base.metadata.clear()
engine = create_engine('mysql+mysqldb://root:199095@localhost/blog', echo=False, convert_unicode=True, pool_size=10,
                       pool_recycle=1800)
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

    def __init__(self, id=None, title=None, content=None, author=None, create_time=None, category=None):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.category = category
        self.create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return 'Article(%d,"""%s""","""%s""", "%s","%s", %d)' % (
            self.id, self.title, self.content, self.author, self.create_time, self.category)


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))

    def __init__(self, name=None):
        self.name = name


    def __repr__(self):
        return 'Tag("{}")'.format(self.name)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    articles = relationship('Article')


Base.metadata.create_all(engine)
