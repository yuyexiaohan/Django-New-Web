# encoding: utf-8
"""
    这个文件是用来将每次返回的信息{code,message,data}三个数据封装为一个模块方便使用。避免每次都将这三个参数反复写入。类似等价与JsonResponse，但是将数据封装，避免每次的数据的重复
    JsonResponse类形式如下：
    classJsonResponse（data，encoder = DjangoJSONEncoder，safe = True，json_dumps_params = None，** kwargs）[source]
 """

from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

# {"code":400,"message":"","data":{}}


def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def ok():
    return result()


def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message='', data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message='', data=None):
    return result(code=HttpCode.servererror, message=message, data=data)
