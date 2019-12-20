// 获取cookies
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
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
$(function () {
   var  submitBtn = $("#submit-btn-add-teacher");
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
               "X-CSRFToken": getCookies("csrf_token")
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

$(function () {
    // var editBtn =
});