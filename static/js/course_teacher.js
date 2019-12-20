
// 加载更多新闻的事件,使用前端数据写加载更多事件
$(function () {
    // var page = 2;
    var loadBtn = $('.load-more-btn');
    loadBtn.click(function () {
        // 通过找选中文件会有active类，这样就会找对应的后面的category_id的方式来加载对于的类别的数据
        var li = $(".list-tab-group li.active");
        var category_id = li.attr("data-category-id");
        //loadBtn.attr('data-page')的到的是一个字符串类型，后面运算，需要转换为整型
        var page = parseInt(loadBtn.attr('data-page'));
        console.log("category_id:",category_id);
        xfzajax.get({
            'url' : '/list/',
            'data': {
                'p' : page,
                'category_id':category_id
            },
            'success' : function (result) {
                // console.log(result);// 打印测试
                var newses = result['data'];
                // console.log(newses); // 打印测试
                if(newses.length > 0){
                    var tpl = template("news-item",{"newses":newses});
                    var newListGroup = $(".news-list-group");
                    newListGroup.append(tpl);
                    page += 1; // 执行完加载后，将page加1，这样就一次为基础进行下一个加载
                    // 在查看此时"加载更多"按钮上的查看page实际值并赋值给page
                    loadBtn.attr('data-page',page);
                    console.log("page:",page);
                }else {
                    window.messageBox.showInfo('没有更多数据了...')
                }

            }
        })
    });
});


function getCookies(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ?r[1] :undefined;
}

// 定义老师信息获取
$(document).ready(function () {
    $.get("/cms/course_teacher/?format=json", function (resp) {
        if(resp.errno === '0'){
            console.log("resp.errno:", resp.data());
        }
    });
});
