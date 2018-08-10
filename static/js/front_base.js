// 前端时间问题

$(function () {
    // console.log(typeof template); // 打印是否定义
    // if(template){
    // template文件如果未在front_base.js之前导入template-wen.js文件，则template就是未定义，这样如果直接使用if(template)就会报错（error：template：undefined）
    if(typeof template != 'undefined'){
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var datets = date.getTime();
            var nows = (new Date()).getTime();
            var timestamp = (nows - datets)/1000;
            if(timestamp < 60){
                return '刚刚';
            }
            else if(timestamp >= 60 && timestamp < 60*60) {
                var minutes = parseInt(timestamp / 60);
                return minutes+'分钟前';
            }
            else if(timestamp >= 60*60 && timestamp < 60*60*24) {
                var hours = parseInt(timestamp / 60 / 60);
                return hours+'小时前';
            }
            else if(timestamp >= 60*60*24 && timestamp < 60*60*24*30) {
                var days = parseInt(timestamp / 60 / 60 / 24);
                return days + '天前';
            }else{
                // %Y/%m/%d %H:%M
                // JS是不支持这种日期格式化的
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minute = date.getMinutes();
                return year+'/'+month+'/'+day+" "+hour+":"+minute;
        }
    };
    }
});


// 首页栏目选中加粗显示功能
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
    var menuLis = $(".menu li"); // 获取li标签，得到一个数组
    // 循环遍历左侧栏目及。menu 下面的li标签
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
