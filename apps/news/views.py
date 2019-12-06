from django.shortcuts import render
from .models import NewCategory, News, Banner
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer, CommentSerializer  # 导入定义序列化
from django.http import Http404
from .forms import AddCommentForm
from .models import Comment
# login_required：只能针对传统的页面跳转（如果没有登录，就跳转到login_url指定的页面）
# 但是他不能处理这种ajax请求。就是说如果通过ajax请求去访问一个需要授权的页面
# 那么这个装饰器的页面跳转功能就不行了,针对Ajax请求的页面跳转自定义一个装饰器
# from django.contrib.auth.decorators import login_required
from apps.xfzauth.decorators import xfz_login_required   # y导入自定义的用于ajax请求的装饰器
# 当我们在查询的条件中需要组合条件时(例如两个条件“且”或者“或”)时。
# 我们可以使用Q()查询对象
from django.db.models import Q


def index(request):
    """新闻显示页,加入轮播图"""
    # newses = News.objects.all()
    # 用于加载界面显示新闻的个数，settings中设置的ONE_PAGE_NEWS_COUNT是1，
    # 这里配置后，界面只会展示1篇文章
    newses = News.objects.select_related('category', 'author')[
        0:settings.ONE_PAGE_NEWS_COUNT]
    categories = NewCategory.objects.all()
    banners = Banner.objects.all()  # 获取轮播图
    # context 中''中的数据是传入HTML模板中的变量，
    # print(type(banners), 'banners:%s' % banners)
    context = {
        'newses': newses,
        'categories': categories,
        'banners': banners  # 将轮播图数据返回给前端
    }
    return render(request, 'news/index.html', context=context)


@require_GET
def news_list(request):
    """
    新闻列表,用于当加载更多时，翻页
    """
    # /news/list/?p=3
    # 对于没有捕获的p参数，我们后面加一个默认参数，避免浏览器获取数据类型错误
    page = int(request.GET.get('p', 1))
    # 分类的id就叫做"category_id"
    category_id = int(request.GET.get('category_id', 0))  # 获取分类id
    # offer,limit
    start = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
    end = start + settings.ONE_PAGE_NEWS_COUNT
    # newses：QuerySet -> [News(),News()] 下面的值
    # newses对象： [{"title":"","content":''},{"title":"","content":''}]
    # newses = list(News.objects.all()[start:end].values())
    # value:将QuerySet中的模型对象（比如News()对象）转换为字典
    # 加list直接强制将QuerySet转换为列表

    # 当定义好Newserializers并引入后，就可以直接使用***serializer定义
    if category_id == 0:
        # 如果category_id等于0，说明用户未创建分类
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start: end]
    serializer = NewsSerializer(newses, many=True)
    return restful.result(data=serializer.data)


def news_detail(request, news_id):
    """新闻详情 """
    try:
        news = News.objects.select_related(
            'category', 'author').get(
            pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404  # 抛出一个404错误，当抛出404时，django就会在根文件中的templates文件调用一个叫做404的文件


@require_POST
@xfz_login_required
def add_comment(request):
    """评论"""
    # 对于django种如果没有登录用户，也还是会有一个request.user ->AnonymousUser的一个假用户，
    # 这个用户数据是不能存储在数据库的
    form = AddCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(
            content=content, news=news, author=request.user)  # 创建评论
        serizlize = CommentSerializer(comment)
        return restful.result(data=serizlize.data)  # 获取数据
    else:
        return restful.params_error(message=form.get_error())


def search(request):
    """查询，返回一个查询页面 """
    q = request.GET.get('q')
    if q:
        # 搜索对象为：title或者content中包含的关键字，有就返回
        newes = News.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q))
        if newes:
            flag = 2
        else:
            page = int(request.GET.get('p', 1))
            start = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
            end = start + settings.ONE_PAGE_NEWS_COUNT
            newes = News.objects.all()[start:end]
            flag = 1
    else:
        page = int(request.GET.get('p', 1))
        start = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
        end = start + settings.ONE_PAGE_NEWS_COUNT
        newes = News.objects.all()[start:end]
        flag = 0

    context = {'newes': newes, 'flag': flag}
    return render(request, 'news/search.html', context=context)
