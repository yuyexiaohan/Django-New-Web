# encoding:utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
# ContentType:用来将模型和app进行关联
from apps.news.models import News, NewCategory, Banner, Comment
from apps.course.models import CourseOrder, Course, CourseCategory
from apps.payinfo.models import PayinfoOrder, Payinfo


class Command(BaseCommand):
    """权限管理"""

    def handle(self, *args, **options):
        # 编辑组/财务组/管理组/超级管理员
        # python manage.py initgroup

        # 1. 编辑权限：编辑文章/轮播图/付费资讯/课程
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Payinfo)
        ]
        # 如果是这里任何一个类型，就将数据查找出来
        edit_permissions = Permission.objects.filter(
            content_type__in=edit_content_types)
        editGroup = Group.objects.create(name='编辑')
        # 将查找后编辑相关的内容创建进去
        editGroup.permissions.set(edit_permissions)

        # 2.财务权限：拥有查看所有订单的权限
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayinfoOrder)
        ]
        finance_permissions = Permission.objects.filter(
            content_type__in=finance_content_types)
        financeGroup = Group.objects.create(name='财务')
        # 将查找后财务相关的内容创建进去
        financeGroup.permissions.set(finance_permissions)

        # 3. 管理员权限：拥有财务和编辑人员的权限
        admin_permissions = edit_permissions.union(
            finance_permissions)  # union将两者权限合二为一
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)

        self.stdout.write(self.style.SUCCESS("初始化分组已经添加成功！"))
