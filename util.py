# encoding:utf8
__author__ = 'brianyang'

import re


def page_slice(url, total, page_num, page_size):
    """
    用来分页，返回上一页和下一页的url
    :param url:
    :param total:
    :param page_num:
    :param page_size:
    :return:
    """
    pre = -1
    behind = -1
    if page_num > 1:
        pre = page_num - 1
    if page_num * page_size < total:
        behind = page_num + 1
    if pre == -1 and behind == -1:
        return 'null', 'null'
    elif pre == -1:
        return 'null', '{}/{}/'.format(url, behind)
    elif behind == -1:
        return '{}/{}/'.format(url, pre), 'null'
    return '{}/{}/'.format(url, pre), '{}/'.format(url, behind)


image_re = re.compile(r"\|img\|(?P<img>.*?)\|(?P<alt>.*?)\|")
paragraph_re = re.compile(r"\|p\|")


def parse_content(content):
    image_parsed = parse_image(content)
    paragraph_parsed = parse_paragraph(image_parsed)
    return paragraph_parsed


def parse_paragraph(content):
    """
    用来对文本中的换行标记进行替换， |p|
    :param content: :return: """
    return paragraph_re.sub('<br />', content)


def parse_image(content):
    """
    用来对文本中的图片标签进行处理， 标签->HTML标记
    |img|http://xxx.jpg|alt|
    :param content:
    :return:
    """

    def parse(matched):
        img = matched.group('img')
        alt = matched.group('alt')
        img = img.replace('\"', '\'')
        return "<img src=\"%s\" alt=\"%s\"/>" % (img, alt)

    return image_re.sub(parse, content)


