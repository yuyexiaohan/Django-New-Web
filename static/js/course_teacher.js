// 获取cookies
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


// 数据post和put方法操作
function submitBtn (type) {

}


// 获取老师信息
$(document).ready(function () {
    $.get("/cms/course_teacher_list/?format=json", function (resp) {
        if(resp){
            $("#course-teacher-list").html(template("course-teacher-list-tmpl", {course_teachers:resp}));
        }else {
            console.log("django-rest-framework没有返回数据！");
        }
    });
});

// 添加老师信息
$(function addTeacher () {
   var  submitBtn = $("#submit-btn-teacher");
    submitBtn.click(function (event) {
        event.preventDefault();
        var teacherName = $("input[name='teacher-name']").val();
        var teacherJobTitle = $("input[name='teacher-job-title']").val();
        var teacherProfile = $("textarea[name='teacher-profile']").val();
        var teacherAvatar = $("input[name='teacher-avatar']").val();
        var data = {
               'username': teacherName,
               'jobtitle': teacherJobTitle,
                'profile': teacherProfile,
                'avatar': teacherAvatar
            };
        $.ajax({
            url: '/cms/course_teacher_list/',
            type: 'post',
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            headers: {
               "X-CSRFToken": getCookies("csrftoken")
            },
            success: function (resp) {
                // console.log("resp:", resp);
                if(resp){
                    console.log("数据提交成功！");
                    window.location.reload(); // 重新加载当前界面
                }else{
                    console.log("添加老师信息失败！");
                }
            }
        });
    });
});

// 编辑老师信息
$(function () {
    // $('#teacher-button').click();
    $("body").on('click',".edit-btn",function () {
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
        // teacherNameFrom.setAttribute("value", teacherName);
        // alert(teacherNameFrom.value);
        // alert(teacherJobTitleFrom.val());
        // alert(teacherProfileFrom.val());
        $('#teacher-button').click();
        $('#submit-btn-teacher').click(function (e) {
            e.preventDefault();
            var newTeacherName = $("textarea[name='teacher-name']").val();
            var newTeacherJobTitle = $("textarea[name='teacher-job-title']").val();
            var newTeacherProfile = $("textarea[name='teacher-profile']").val();
            var newTeacherAvatar = $("textarea[name='teacher-avatar']").val();
            var data = {
                'username': newTeacherName,
                'jobtitle': newTeacherJobTitle,
                'profile': newTeacherProfile,
                'avatar': newTeacherAvatar
            };
            $.ajax({
                url: '/cms/course_teacher_list/' + teacherId + '/',
                type: 'put',
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
                headers: {
                    "X-CSRFToken": getCookies("csrftoken")
                },
                success: function (resp) {
                    if (resp) {
                        console.log("数据提交成功！");
                        // window.location.reload(); // 重新加载当前界面
                    } else {
                        console.log("修改老师信息失败！");
                    }
                }
            });
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