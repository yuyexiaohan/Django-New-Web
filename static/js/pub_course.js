

// 课程发布部分的课程简介的编辑部分的Ueditor的调用
$(function () {
    // 定义一个editor进行传参数
    window.ue = UE.getEditor('editor',{
        'serverUrl':'/ueditor/upload/'
        // 也可以加入高度，宽度，可以参考cms下的write_news.js
    });
});

// 
$(function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function () {
        // 阻止传统表单上传数据的默认行为，如果没有加这个，在后台的
        // return restful.ok() 就会返回一个错误信息直接在页面
       event.preventDefault();
       // 从前端的html文件中获取变量值
       var title = $("#title-input").val();
       var category_id = $("#category-select").val();
       var teacher_id = $("#teacher-select").val();
       var video_url = $("#video-input").val();
       var cover_url = $("#cover-input").val();
       var price = $("#price-input").val();
       var duration = $("#duration-input").val();
       var profile = window.ue.getContent();

       // 通过Ajax请求发送返回给后端
        xfzajax.post({
            'url':'/cms/pub_course/',
            'data':{
                'title':title,
                'category_id':category_id,
                'teacher_id':teacher_id,
                'video_url':video_url,
                'cover_url':cover_url,
                'price':price,
                'duration':duration,
                'profile':profile
            },
            'success':function (result) {
                if(result['code'] === 200){
                    // 验证成功后，刷新界面
                    window.location = window.location.href;
                }
            }
        });
    });
});