// 获取cookies
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}







// 编辑老师信息
$(function () {
    $('#submit-btn-teacher').click(function (e) {
        e.preventDefault();
        var teacherId = $(".modal-body").attr('data-id');
        var newTeacherName = $("input[name='teacher-name']").val();
        var newTeacherJobTitle = $("input[name='teacher-job-title']").val();
        var newTeacherProfile = $("input[name='teacher-profile']").val();
        var newTeacherAvatar = $("input[name='teacher-avatar']").val();
        var data = {
            'username': newTeacherName,
            'jobtitle': newTeacherJobTitle,
            'profile': newTeacherProfile,
            'avatar': newTeacherAvatar
        };
        if(data){
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
                    window.location.replace('/cms/course_teacher/'); // 重新加载当前界面
                } else {
                    console.log("修改老师信息失败！");
                }
            }
        });
        }else{
            alert("信息输入有误！")
        }
    });
});

