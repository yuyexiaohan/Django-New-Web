
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

// 定义点击分类获取分类新闻
$(function () {
    // 获取category分类的标签元素，可以通过class获取ui标签，然后同children获取ui下的子元素
   var categoryUl = $(".list-tab-group");
   var liTags = categoryUl.children(); // children 是直接获取categorUI标签下的子元素（子元素：指这个标签的下一级元素，不包括下2级等元素）
    var loadBtn = $(".load-more-btn");
   liTags.click(function () {
        var li = $(this);
        var categoryId = li.attr('data-category-id');
        xfzajax.get({
            'url':'/list/',
            'data': {
                'category_id':categoryId
            },
            'success': function (result) {
                // console.log(result);// 打印测试
                var newses = result['data'];
                // console.log(newses); // 打印获取的新闻
                var tpl = template("news-item",{"newses":newses}); // 将查询到的新闻内容放到显示界面，并清除之前显示的数据
                var newsListGroup = $(".news-list-group");
                // empay: 可以将newsListGroup下的所有标签都清除掉
                newsListGroup.empty();
                newsListGroup.append(tpl);// 添加新的新闻数据
                li.addClass('active').siblings().removeClass('active');
                loadBtn.attr('data-page',2); // 一旦点击分类标签后，每页展示内容默认为2
            }
        });
   });
});
