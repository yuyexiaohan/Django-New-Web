from apps.forms import FormMixin  # 导入错误信息反馈表单
from django import forms
from apps.news.models import News, Banner  # 导入创建的数据库模型
from apps.course.models import Course  # 导入发布课程的模型


class EditNewsCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "必须传入一个分类id!"})
    name = forms.CharField(max_length=100, min_length=1)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        fields = ('title', 'desc', 'thumbnail', 'content')
        error_messages = {
            'category': {
                'required': '必须传分类的id！'
            },
            'title': {
                'min_length': '最小长度不小于1个字符！'
            }
        }


'''定义一个编辑新闻的表单函数'''
# 可以继承WriteNewsForm


class EditNewsForm(WriteNewsForm):
    pk = forms.IntegerField()


'''定义一个轮播图的数据表单，用来存放前端post获取的数据，然后便于存放在数据库对应的模型中'''


class AddBanner(forms.ModelForm, FormMixin):
    # 导入模型表单和定义的输出错误信息的FormMixin表单
    # Meta 是干什么的？
    class Meta:
        model = Banner
        fields = ('image_url', 'link_to', 'priority')


'''定义一个编辑轮播图的表单，用来pk作为轮播图id，传入轮播图链接，跳转链接，优先级等信息'''


class EditBannerForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()  # 因为模板中定义Id，这里表单中需要自己定义

    class Meta:
        model = Banner
        fields = ('image_url', 'link_to', 'priority')


'''定义一个发布课程表单，内容有课程标题/课程分类/讲师/视频地址/封面图/价格/课程时长/课程简介等'''


class EditCoursesCategoryForm(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "必须传入一个分类id!"})
    name = forms.CharField(max_length=100, min_length=1)


class AddCourseForm(forms.ModelForm, FormMixin):
    # 定义两个表单变量，分类id和老师id
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        # 我们需要表单获取模型中的参数，这里使用exclude方法，排除一些参数，保留其它未排除的参数
        exclude = ('pub_time', 'category', 'teacher')
