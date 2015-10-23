__author__ = 'brianyang'


def page_slice(url, total, page_num, page_size):
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
