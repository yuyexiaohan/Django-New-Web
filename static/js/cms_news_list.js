// 新闻管理界面相关功能

// 按照http://www.bootcss.com/p/bootstrap-datetimepicker/的说明对开始核结束日期参数进行说明
$(function () {
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var option = {
        'autoclose':true,
        'format':'yyyy/mm/dd',
        'startDate':'2018/06/01',
        'endDate':todayStr,
        'language':'zh-CN',
        'todayHighlight':true,
        'clearBtn':true,
        'showButtonPanel':true,
        // 'todayBtn':'linked'
    };
    // 初始化开始日期,datepicker模块定义的方法
    $("input[name='start']").datepicker(option);
    // 初始化结束日期
    $("input[name='end']").datepicker(option);

});

/* 定义一个点击删除新闻的函数 */

$(function () {
   var deleteBtn = $(".delete-btn");
   deleteBtn.click(function () {
       var pk = $(this).attr('data-news-id');
       xfzalert.alertConfirm({
           'text':'确定要删除这篇新闻吗？',
           'confirmCallback':function () {
               xfzajax.post({
                   'url':'/cms/delete_news/',
                   'data':{
                       'pk':pk
                   },
                   'success':function (result) {
                       if(result['code']===200){
                           window.location.reload(); // 刷新界面：方法1
                           window.location = window.location.href; // 刷新界面：方法2（相比方法1在各个浏览器中兼容性较好，方法1在火狐中可能存在无法刷新）
                       }
                   }
               });
           }
       })
   });
});
