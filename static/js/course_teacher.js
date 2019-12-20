
function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ?r[1] :undefined;
}

// 老师信息获取
$(document).ready(function () {
    $.get("/cms/course_teacher_list/?format=json", function (resp) {
        if(resp){
            $("#course-teacher-list").html(template("course-teacher-list-tmpl", {course_teachers:resp}));
        }else {
            console.log("django-rest-framework没有返回数据！");
        }
    });
});

// 创建老师信息
$(document).ready(function () {


   $.post("/cms/course_teacher_list/?format=json", function (resp) {
       
   }) ;
});