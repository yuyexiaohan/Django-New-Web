/*
// 缩略图文件验证及文件上传到我们自己的服务器
$(function () {
    var uploadBtn = $('#upload-btn');
    // 这里不同之前需要监听click点击事件，这里只需要监听打开文件选择上传的动作，这里使用change ,event是指当前点击的事件
    uploadBtn.change(function (event) {
        // event.preventDefault(); // 阻止将表单发送到数据库的默认行为。但是这里使用了input的file数据类型，该标签不会进行默认操作，所以这里也可以省去。
        var file = this.files[0]; //使用this直接指向这个文件，获取该文件
        var formData = new FormData(); //构建成表单体，构造表单数据
        formData.append('upfile',file); // 获取表单数据，获取变量取决于后端定义的变量'upfile'
        // 使用Ajax将数据传输进去
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false, //'processDate'是一个默认为Ture的用来处理data中的数据，这里配置围为false，不让做相关处理
            'contentType':false, // 默认也是Ture,会将文件变成一种js文件，这里实际是上传一张照片，所以设置为false不做处理
            'success': function (result) {
                if (result['code'] === 200){
                    // 默认在网页中答应查看result
                    // console.log(result);
                    var url = result['data']['url'];
                    var thumbnailInput = $("input[name='thumbnail']");
                    thumbnailInput.val(url);
                }
            }
        });
    });
});
*/


// 使用七牛云上传文件
$(function () {
    // progressGroup 是用来进行控制进度条是否需要显示的
    var progressGroup = $("#progress-group");
    // progressBar 是用来控制进度条的宽度
    var progressBar = $("#progress-bar");

    function progress(response) {
        var percent = response.total.percent;
        var percentText = percent.toFixed(0) + '%'; // .toFixed(0)代表小数点后面给0位
        console.log('##################');
        console.log(percent);
        console.log('##################');
        progressBar.css({"width":percentText});
        progressBar.text(percentText);
    }
    function error(err) {
        console.log('==========');
        console.log(err);
        console.log('==========');
        window.messageBox.showError(err.message); //输出错误信息

        progressGroup.hide(); // 错误出现后隐藏

    }
    function complete(response) {
        // 内部含有两个值，一个是哈希值，一个是类名
        var key = response.key;
        var domain = 'http://pbomppzdt.bkt.clouddn.com/'; // 七牛云给出存储空间的外链，可以根据使用七牛云空间的不同进行更改
        var url = domain + key;
        var thumbnailInput = $("input[name='thumbnail']");
        thumbnailInput.val(url);

        progressGroup.hide(); // 进度条完成后隐藏
        progressBar.css({"width":'0'}); // 上传完成后，就将宽度调整为0
        progressBar.text('0%'); // 提示的文字宽度也变成0
    }

    var uploadBtn = $('#upload-btn');
    // 这里不同之前需要监听click点击事件，这里只需要监听打开文件选择上传的动作，这里使用change
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url':'/cms/qntoken/',
            'success':function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    // console.log(token); // 打印测试
                    var key = file.name;
                    var putExtra = {
                        fname:key,
                        params:{},
                        mimeType:['image/png','image/jpeg','image/gif','image/jpg']
                    };
                    var config = {
                        useCdnDomain:true,
                        region:qiniu.region.z0 //qiniu.region.z0: 代表华东区域 qiniu.region.z1: 代表华北区域 qiniu.region.z2: 代表华南区域 qiniu.region.na0: 代表北美区域 qiniu.region.as0: 代表新加坡区域 根据实际情况进行修改
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next':progress,
                        'error':error,
                        'complete':complete
                    });
                    progressGroup.show();
                }
            }
        });
    });
});

// 文本编辑器
$(function () {
    // window.ue 是将ue这个变量作为全局变量来定义
    window.ue = UE.getEditor('editor',{
        // 官方文档中给出前端的高度配置说明
        "initialFrameHeight":400 , //初始化编辑器宽度
        'serverUrl':'/ueditor/upload/' // 服务器统一请求接口路径
    });
});

// 新闻发布
$(function () {
    var submiBtn = $('#submit-btn');
    submiBtn.click(function (event) {
        event.preventDefault(); // 去除原有的格式
        var btn = $(this); // 当前点击的这个按钮
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var category = $("select[name='category']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var news_id = btn.attr('data-news-id');
        var url = '';
        if(news_id){
            url = '/cms/edit_news/';
        }else {
            url = '/cms/write_news/'
        }
        xfzajax.post({
            'url':url,
            'data': {
                'title':title,
                'desc':desc,
                'category':category,
                'thumbnail':thumbnail,
                'content':content,
                'pk':news_id
            },

            'success':function (result) {
                if (result['code'] === 200){

                    xfzalert.alertSuccess('新闻发布成功！',function () {
                        url = '/cms/news_list/';
                        window.location.reload(); // 重新加载当前界面

                    });
                }
            }
        });
    });
});


/*
// t
$(function () {
    // progressGroup：用来控制整个进度条是否需要显示的
    var progressGroup = $("#progress-group");
    // progressBar：用来控制这个进度条的宽度
    var progressBar = $(".progress-bar");

    function progress(response) {
        var percent = response.total.percent;
        var percentText = percent.toFixed(0) + '%';
        console.log('****************');
        console.log(percent);
        console.log('****************');
        progressBar.css({"width":percentText});
        progressBar.text(percentText);
    }

    function error(err) {
        console.log('========');
        console.log(err);
        console.log('========');
        window.messageBox.showError(err.message);

        progressGroup.hide();
    }

    function complete(response) {
        // hash key
        var key = response.key;
        var domain = 'http://7xqenu.com1.z0.glb.clouddn.com/'; //实际看七牛上空间给与的外链
        var url = domain + key;
        var thumbnailInput = $("input[name='thumbnail']");
        thumbnailInput.val(url);

        progressGroup.hide();
        progressBar.css({"width":'0'});
        progressBar.text('0%');
    }

    var uploadBtn = $("#upload-btn");
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    var key = file.name;
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg', 'image/gif','video/x-ms-wmv']
                    };
                    var config = {
                        useCdnDomain: true,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next': progress,
                        'error': error,
                        'complete': complete
                    });
                    progressGroup.show();
                }
            }
        });
    });
});
*/
/*
$(function () {
    window.ue = UE.getEditor('editor',{
        "initialFrameHeight": 400,
        'serverUrl': '/ueditor/upload/'
    });
});
*/
/*
$(function () {
    var submiBtn = $("#submit-btn");
    submiBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var category = $("select[name='category']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        xfzajax.post({
            'url': '/cms/write_news/',
            'data': {
                'title': title,
                'desc': desc,
                'category': category,
                'thumbnail': thumbnail,
                'content': content
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
});
*/