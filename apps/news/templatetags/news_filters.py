"""
编写过滤器，使用时需要在对应模板（HTML）中加载
功能：规范发布时间显示
"""

from django import template
from datetime import datetime
from django.utils.timezone import now as now_func  # 配置当前时间的工具
from django.utils.timezone import localtime  # 导入一个本地时间

register = template.Library()


@register.filter
def time_since(value):
    """
    time距离现在的时间间隔
    1.如果时间间隔小于1分钟以内，那么就显示“刚刚”
    2.如果是大于1分钟小于1小时，那么就显示“xx分钟前”
    3.如果是大于1小时小于24小时，那么就显示“xx小时前”
    4.如果是大于24小时小于30天以内，那么就显示“xx天前”
    5.否则就是显示具体的时间
    2017/10/20 16:15
    """
    if not isinstance(value, datetime):
        return value

    # aware time：清醒的时间（清醒的知道自己这个时间代表的是哪个时区的）
    # navie time：幼稚的时间（不知道自己的时间代表的是哪个时区）

    # now = datetime.now() # 这样得到的是navie time 幼稚时间
    now = now_func()
    # 这样得到的就是一个清新的时间aware time，不这样做就会报错，因为value是我们定义的上海的时间，是一个清醒时间，如果使用"now = datetime.now()"得到的幼稚时间就不能和清醒时间作算术，会报错
    # datetime
    timestamp = (now - value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60 * 60:
        minutes = int(timestamp / 60)
        return '%s分钟前' % minutes
    elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
        hours = int(timestamp / 60 / 60)
        return '%s小时前' % hours
    elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
        days = int(timestamp / 60 / 60 / 24)
        return '%s天前' % days
    else:
        return value.strftime("%Y/%m/%d %H:%M")


"""添加一个时间过滤器"""


@register.filter
def time_format(value):
    if not isinstance(value, datetime):
        return value
    return localtime(value).strftime("%Y/%m/%d %H:%M:%S")
# localtime 获取本地时间，strftime变成规范的年月日，时分秒
