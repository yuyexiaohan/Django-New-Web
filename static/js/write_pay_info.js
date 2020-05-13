// 获取cookies
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;

}


// 使用七牛云上传文件
$(function () {
    // progressGroup 是用来进行控制进度条是否需要显示的
    var progressGroup = $("#progress-group");
    // progressBar 是用来控制进度条的宽度
    var progressBar = $(".progress-bar");

    function progress(response) {
        var percent = response.total.percent;
        var percentText = percent.toFixed(0) + '%'; // .toFixed(0)代表小数点后面给0位
        progressBar.css({"width":percentText});
        progressBar.text(percentText);
    }
    function error(err) {
        window.messageBox.showError(err.message); //输出错误信息
        progressGroup.hide(); // 错误出现后隐藏

    }
    function complete(response) {
        // 内部含有两个值，一个是哈希值，一个是类名
        var key = response.key;
        var domain = 'http://achjiang.cn/';
        // 七牛云给出存储空间的外链，可以根据使用七牛云空间的不同进行更改
        var url = domain + key;
        var thumbnailInput = $("textarea[name='thumbnail']");
        thumbnailInput.html(url);
        console.log("上传七牛云图片地址：",url);
        $('#teacher-button').click();

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
                        region:qiniu.region.z0
                        /*qiniu.region.z0: 代表华东区域 qiniu.region.z1: 代表华北区域 qiniu.region.z2: 代表华南区域 qiniu.region.na0: 代表北美区域 qiniu.region.as0: 代表新加坡区域 根据实际情况进行修改*/
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



// 编辑付费知识信息
function submitBtn(event, payInfoId) {
    event.preventDefault();
    var method;
    var payInfoTitle = $("#pay-info-title").val();
    var payInfoProfile = $("#pay-info-profile").val();
    var payInfoPrice = $("#pay-info-price").val();
    var payInfoPath = $("#thumbnail-form").val();
    data = {
        'title': payInfoTitle,
        'profile': payInfoProfile,
        'price': payInfoPrice,
        'path': payInfoPath
    };

    if(payInfoId !== ''){
        url = 'cms/pay_info/' + payInfoId + '/'
    }else{
        url = 'cms/payinfo/'
    }
    if (window.flag === 0){
        method = 'post'
    }
    if (window.flag === 1){
        method = 'put'
    }
    $.ajax({
        url: url,
        type: method,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookies("csrftoken")
        },
        success: function(resp){
            if(resp){
                alert("信息保存成功！")
                window.location.reload();
            }else{
                alert("信息保存失败！")
            }
        }
    })

}


// 新增pay-info
$(function addPayInfo() {
    $("#submit-pay-info").click(function () {
      submitBtn(event, '');
    })
});


// 编辑pay-info
$(function editPayInfo() {


})