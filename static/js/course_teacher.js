// 获取cookies
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


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