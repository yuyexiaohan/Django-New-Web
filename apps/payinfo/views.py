import os
from hashlib import md5  # 导入md5加密

from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Payinfo, PayinfoOrder
from utils import restful


def index(request):
    """付费资讯"""
    payinfos = Payinfo.objects.all()
    context = {
        'payinfos': payinfos
    }
    return render(request, 'payinfo/payinfo.html', context=context)


@login_required(login_url='/account/login/')
def payinfo_order(request):
    """付费资讯的支付"""
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    price = payinfo.price
    if price == 0:
        return redirect(
            reverse("payinfo:download_payinfo") +
            "?payinfo_id=%s" %
            payinfo.pk)
    else:
        buyed = PayinfoOrder.objects.filter(
            buyer=request.user, payinfo=payinfo, status=2)
        if buyed:
            return redirect(
                reverse("payinfo:download_payinfo") +
                "?payinfo_id=%s" %
                payinfo.pk)

    order = PayinfoOrder.objects.create(
        buyer=request.user,
        amount=payinfo.price,
        payinfo=payinfo,
        status=1)

    context = {
        'payinfo': payinfo,
        'order': order,
        # /payinfo/notify_url/
        'notify_url': request.build_absolute_uri(reverse('payinfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payinfo:download_payinfo') + "?payinfo_id=%s" % payinfo.pk)
    }
    return render(request, 'payinfo/create_order.html', context=context)


def order_key(request):
    """支付加密"""
    goodsname = request.POST.get('goodsname')
    istype = request.POST.get('istype')
    notify_url = request.POST.get('notify_url')
    orderid = request.POST.get('orderid')
    price = request.POST.get('price')
    return_url = request.POST.get('return_url')

    token = 'e6110f92abcb11040ba153967847b7a6'
    uid = '49dc532695baa99e16e01bc0'
    orderuid = str(request.user.pk)

    print('goodsname:', goodsname)
    print('istype:', istype)
    print('notify_url:', notify_url)
    print('orderid:', orderid)
    print('price:', price)
    print('return_url:', return_url)
    print('token:', token)
    print('orderuid:', orderuid)

    key = md5(
        (goodsname +
         istype +
         notify_url +
         orderid +
         orderuid +
         price +
         return_url +
         token +
         uid).encode("utf-8")).hexdigest()
    # key = md5 ("".join ([goodsname, istype, notify_url, orderuid, orderuid, price, return_url, token, uid])
    # .encode ("utf-8")).hexdigest ()
    return restful.result(data={'key': key})


@csrf_exempt
def notify_view(request):
    """支付链接视图函数"""
    orderid = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()


def download_payinfo(request):
    """下载文件视图函数"""
    # 如果用户没有购买这个付费信息时，那么不能够让他下载
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    price = payinfo.price
    if price != 0:
        buyed = PayinfoOrder.objects.filter(
            payinfo=payinfo, buyer=request.user, status=2)
        if not buyed:
            return redirect(reverse('payinfo:index'))
    path = payinfo.path
    # 作为一个附件的形式下载，而不是作为一个普通的文件下载
    response = FileResponse(
        open(
            os.path.join(
                settings.MEDIA_ROOT,
                path),
            'rb'))
    # HTTP Content-Type标头中包含的值，包括MIME类型规范和字符集编码。
    # 如果 content_type指定，则使用其值。
    response['Content-Type'] = 'image/jpeg'
    # 'Content-Disposition'告诉浏览器将响应视为文件附件
    # >>> response = HttpResponse(my_data, content_type='application/vnd.ms-excel')
    # >>> response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    # path=/20180725/xx.jpg = ['',20180725,xx.jpg]
    response['Content-Disposition'] = 'attachment;filename="%s"' % path.split(
        "/")[-1]
    return response
