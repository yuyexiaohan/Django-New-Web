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


// 设置全局变量flag，用于判别submitBtnFun();函数的提交方法'post','put'
// 当flag = 0; method = 'post';
// 当flag = 1; method = 'put';
window.flag = 0;


// 数据提交方法
function submitBtnFun(event,teacherId) {
        event.preventDefault();
        var teacherName = $("textarea[name='teacher-name']").val();
        var teacherJobTitle = $("textarea[name='teacher-job-title']").val();
        var teacherProfile = $("textarea[name='teacher-profile']").val();
        var teacherAvatar = $("textarea[name='teacher-avatar']").val();
        var data = {
               'username': teacherName,
               'jobtitle': teacherJobTitle,
                'profile': teacherProfile,
                'avatar': teacherAvatar
            };
        if(teacherId !== ""){
            url = '/cms/course_teacher_list/'+ teacherId + '/'
        }else{
            url = '/cms/course_teacher_list/'
        }
        if(window.flag===0){
            method = 'post'
        }if(window.flag === 1){
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
            success: function (resp) {
                if(resp){
                    console.log("数据提交成功！");
                    window.location.reload(); // 重新加载当前界面
                }else{
                    console.log("添加老师信息失败！");
                }
            }
        });
    }


// 老师信息js渲染方法
function getTeacherInfo () {
    $.get("/cms/course_teacher_list/?format=json", function (resp) {
        if(resp){
            $("#course-teacher-list").html(template("course-teacher-list-tmpl", {course_teachers:resp}));
        }else {
            console.log("django-rest-framework没有返回数据！");
        }
    });
}


// 获取老师信息
$(document).ready(function () {
    getTeacherInfo();
    // $.get("/cms/course_teacher_list/?format=json", function (resp) {
    //     if(resp){
    //         $("#course-teacher-list").html(template("course-teacher-list-tmpl", {course_teachers:resp}));
    //     }else {
    //         console.log("django-rest-framework没有返回数据！");
    //     }
    // });
});


// 添加老师信息
$(function addTeacher () {
    $("#submit-btn-teacher").click(function () {
        submitBtnFun(event, '');
    })
});


// 编辑老师信息
$(function editTeacher () {
     $("body").on('click',".edit-btn",function () {
        window.flag = 1;  // 设置全局变量flag=1，用于判别提交方法为'put'
        var currentBtn = $(this);

        // 获取当前老师信息
        var tr = currentBtn.parent().parent();
        var teacherId = tr.attr('data-pk');
        var teacherName = tr.attr('data-name');
        var teacherJobTitle = tr.attr('data-jobtitle');
        var teacherProfile = tr.attr('data-profile');
        var teacherAvatar = tr.attr('data-avatar');

        // // 获取编辑from表单各标签信息
        var teacherNameFrom = $("textarea[name='teacher-name']");
        var teacherJobTitleFrom = $("textarea[name='teacher-job-title']");
        var teacherProfileFrom = $("textarea[name='teacher-profile']");
        var teacherAvatarFrom = $("textarea[name='teacher-avatar']");
        var formTitle = $('#exampleModalLabel');
        formTitle.value = "修改老师信息";
        teacherNameFrom.html(value = teacherName);
        teacherJobTitleFrom.html(value = teacherJobTitle);
        teacherProfileFrom.html(value = teacherProfile);
        teacherAvatarFrom.html(value = teacherAvatar);
        $('#teacher-button').click();
        $('#submit-btn-teacher').click(function () {
        submitBtnFun(event,teacherId);
        });
    });
});


// 删除老师信息
$(function () {
    $("body").on('click',".delete-btn",function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var teacherId = tr.attr('data-pk');
        xfzalert.alertConfirm({
           'text': '确定删除该老师的信息吗？',
            // 如果确定执行函数
           'confirmCallback':function () {
               $.ajax({
                    url: '/cms/course_teacher_list/' + teacherId + '/',
                    type: 'delete',
                    contentType: 'application/json',
                    headers: {
                        "X-CSRFToken": getCookies('csrftoken')
                    },
                    success: function () {
                        console.log("删除成功！");
                        window.location.reload();
                    },
                    fail: function () {
                        console.log("删除数据失败！")
                    }
               })
           }
        });
    })
});