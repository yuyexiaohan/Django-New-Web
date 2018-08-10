// cms页面内容选中active选中显示功能的实现

$(function () {
    // 完整域名：http://127.0.0.1:8000/cms/staffs
    var url = window.location.href; // 返回本地地址
    // http:
    var protocol = window.location.protocol;
    // 127.0.0.1:8000
    var host = window.location.host;
    var domain = protocol + '//'+ host;
    // console.log(domain); // 打印测试域名
    var path = url.replace(domain,'');
    // 获取所有管理界面文件的url
    var menuLis = $(".sidebar-menu li"); // 获取li标签，得到一个数组
    // 循环遍历左侧栏目及。sidebar-menu 下面的li标签
    for(var index=0;index<menuLis.length;index++){
        var li = $(menuLis[index]); // 获取对应位置的li标签
        var a = li.children("a"); // 获取li标签下的子类a标签
        var href = a.attr("href"); // 获取a标签的href属性
        // 判断，如果href与之前获得的当前path相同，则添加选中的active属性
        if(href === path){
            li.addClass("active");
        }
    }
});

