// 定义一个js文件用于新闻类别的添加和删除，以及相关信息的提示

// 添加分类部分
$(function () {
    var addBtn = $("#add-btn");
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title':'添加新闻分类',
            'placeholder':'请输入新闻分类',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/add_news_category/',
                    // 注意url前后的/线
                    'data':{
                        'name':inputValue
                    },
                    'success':function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }
                        else {
                            // 如果返回的不是200则将弹出信息框关闭
                            xfzalert.close();
                            // 将信息加载到页面上
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });

    });
});


// 编辑分类
$(function () {
   var editBtn = $('.edit-btn');
   editBtn.click(function () {
       var currentBtn = $(this);
        var tr = currentBtn.parent().parent(); // 找button的上两级标签也就是爷爷类
       var pk = tr.attr('data-pk'); // 通过attr拿到id
       var name = tr.attr('data-name');// 通过attr拿到id
       xfzalert.alertOneInput({
           // 弹出信息窗对应参数定义
          'title':'请输入新的名称',
          'placeholder':'请输入分类名称',
           'value':name,
           // 如果点击确认后，执行后面操作
           'confirmCallback':function (inputValue) {
              // console.log(inputValue); // 打印传入的值
               //使用Ajax的post请求
               xfzajax.post({
                   // url执行执行的路由接口，注意其中路经前后部分与urls文件中的路由一致，如果后面加有'/'，则该url也要加入
                   'url':'/cms/edit_news_category/',
                   //返回数据，pk/name是指通过指定前端的id获取对应分类category中的id和名称
                   'data':{
                       'pk': pk,
                       'name': inputValue
                   },
                   // 如果成功就执行函数
                    'success':function (result) {
                       // 进行判断，如果返回的代码是200即成功，则执行后面操作
                       if(result['code'] === 200){
                           // 重新加载本地页面
                            window.location.reload();
                        }
                    }
               });
           }
       });
   });
});



// 删除分类

$(function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var currentBtn = $(this)
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'text':'你确认要删除该分类吗？',
            // 如果用户点击了确认，执行后面的操作
            'confirmCallback':function () {
                // 执行Ajax请求
                xfzajax.post({
                    'url':'/cms/delete_news_category/',
                    'data':{
                      'pk':pk
                    },
                    // 如果成功则执行下面操作
                    'success':function (result) {
                        if (result['code'] === 200){
                            // 重新加载页面
                            window.location.reload();
                        }
                    }
                });
            }
        });
    })
})



// 老师的代码
// 添加分类
// $(function () {
//     var addBtn = $("#add-btn");
//     addBtn.click(function () {
//         xfzalert.alertOneInput({
//             'title': '添加新闻分类',
//             'placeholder': '请输入新闻分类',
//             'confirmCallback': function (inputValue) {
//                 xfzajax.post({
//                     'url': '/cms/add_news_category/',
//                     'data': {
//                         'name': inputValue
//                     },
//                     'success': function (result) {
//                         if(result['code'] === 200){
//                             window.location.reload();
//                         }else{
//                             xfzalert.close();
//                             window.messageBox.showError(result['message']);
//                         }
//                     }
//                 });
//             }
//         });
//     });
// });
// // 编辑分类
// $(function () {
//     var editBtn = $('.edit-btn');
//     editBtn.click(function () {
//         var currentBtn = $(this);
//         var tr = currentBtn.parent().parent();
//         var pk = tr.attr('data-pk');
//         var name = tr.attr('data-name');
//         xfzalert.alertOneInput({
//             'title': '请输入新名称',
//             'placeholder': '请输入分类名称',
//             'value': name,
//             'confirmCallback': function (inputValue) {
//                 xfzajax.post({
//                     'url': '/cms/edit_news_category/',
//                     'data': {
//                         'pk': pk,
//                         'name': inputValue
//                     },
//                     'success': function (result) {
//                         if(result['code'] === 200){
//                             window.location.reload();
//                         }
//                     }
//                 });
//             }
//         });
//     });
// });
//
// // 删除分类
// $(function () {
//     var deleteBtn = $('.delete-btn');
//     deleteBtn.click(function () {
//         var currentBtn = $(this);
//         var tr = currentBtn.parent().parent();
//         var pk = tr.attr('data-pk');
//         xfzalert.alertConfirm({
//             'text': '您确定要删除这个分类吗？',
//             'confirmCallback': function () {
//                 xfzajax.post({
//                     'url': '/cms/delete_news_category/',
//                     'data': {
//                         'pk': pk
//                     },
//                     'success': function (result) {
//                         if(result['code'] === 200){
//                             window.location.reload();
//                         }
//                     }
//                 });
//             }
//         });
//     });
// });
