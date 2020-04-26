# Django-New-Web
基于Django做的一个新闻网站，有新闻展示、搜索、在线视频播放、资源下载、订单支付、后台CMS管理等功能
1. 下载文件到本地，创建一个虚拟环境后，使用`pip install -r requirements.txt` 安装模块
2. 创建`config.py`文件,示例如下：
```python
    """
    # config.py文件相关参数配置
    # 文件路径/diango_01/config.py
    """

    # 数据库
    MYSQL_NAME = ''
    MYSQL_USER = ''
    MYSQL_PASSWORD = ''
    MYSQL_HOST = ''
    MYSQL_POST = ''
    
    # 阿里云短信服务
    ALI_ACCESS_KEY_ID = ""
    ALI_ACCESS_KEY_SECRET = ""
    ALI_SIGN_NAME = ""
    ALI_TEMPLATE_CODE = ""
    
    # 七牛云存储
    QINIU_ACCESS_KEY = ''
    QINIU_SECRET_KEY = ''
    QINIU_BUCKET_NAME = ''
    QINIU_DOMAIN = ''
    
    # 百度云点播
    BAIDU_CLOUD_USER_ID = ""
    BAIDU_CLOUD_USER_KEY = ''
    
    # 支付pypay
    PAY_TOKEN = ''
    PAY_UID = ''
```

3. 环境配置完成后，使用`python manage.py runserver 0.0.0.0 8000`命令运行系统
4. 在浏览器中输入`127.0.0.1:8000`查看运行项目
