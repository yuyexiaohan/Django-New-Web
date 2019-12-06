from apps.forms import FormMixin  # 导入错误信息反馈表单
from django import forms
from apps.news.models import News, Banner  # 导入创建的数据库模型
from apps.course.models import Course  # 导入发布课程的模型
from apps.xfzauth.models import User


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


class EditNewsForm(WriteNewsForm):
    """编辑新闻"""
    pk = forms.IntegerField()


class AddBannerForm(forms.ModelForm, FormMixin):
    # 导入模型表单和定义的输出错误信息的FormMixin表单
    # Meta 是干什么的？
    class Meta:
        model = Banner
        fields = ('image_url', 'link_to', 'priority')


class EditBannerForm(forms.ModelForm, FormMixin):
    """用来pk作为轮播图id，传入轮播图链接，跳转链接，优先级等信息"""
    pk = forms.IntegerField()  # 因为模板中定义Id，这里表单中需要自己定义

    class Meta:
        model = Banner
        fields = ('image_url', 'link_to', 'priority')


class EditCoursesCategoryForm(forms.Form, FormMixin):
    """
    发布课程表单，内容有课程标题/课程分类/讲师/视频地址/封面图/价格/课程时长/课程简介等
    """
    pk = forms.IntegerField(error_messages={"required": "必须传入一个分类id!"})
    name = forms.CharField(max_length=100, min_length=1)


class AddCourseForm(forms.ModelForm, FormMixin):
    # 定义两个表单变量，分类id和老师id
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        # 表单获取模型中的参数，
        # 这里使用exclude方法，排除一些参数，保留其它未排除的参数
        exclude = ('pub_time', 'category', 'teacher')


class EditUserCenterForm(forms.ModelForm, FormMixin):
    """个人信息表单"""
    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        error_messages={"required": "必须输入手机号码！",
                        "min_length": "手机号码个数必须11位！",
                        "max_length": "手机号码个数必须为11位！"
                        })
    username = forms.CharField(
        max_length=20,
        min_length=3,
        error_messages={
            "required": "请输入用户名！",
            "min_length": "用户名最少不能少于3个字符！",
            "max_length": "用户名最多不能多于20个字符！"
            })

    class Meta:
        model = User
        # exclude = {} # 排除部分参数
        fields = {"telephone", "username"}
        # fields = "__all__"  # 全部参数
