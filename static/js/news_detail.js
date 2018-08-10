// 定义评论部分
$(function () {
    var submitBtn = $('#submit-comment-btn'); // id形式是#+id'',类是.+class
    var textarea = $('.comment-textarea');
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-news-id');
        // Ajax请求获取post请求的数据
        xfzajax.post({
            'url':'/add_comment/',
            'data':{
                'content':content,
                'news_id':news_id
            },
            // 成功，执行如下操作
            'success':function (result) {
                if(result['code'] === 200){
                    console.log(result);// 打印获取的内容，有code,data(data包括：author，content，id，pub_time等信息，这些都是之前定义序列化获取的文件),message
                    var comment = result['data']; //将数据赋值给comment
                    var tpl = template('comment-item',{"comment":comment}); //查找id为comment-item，并将数据comment传入
                    var commentGroup = $('.comment-list-group');// 获取存储评论的容器，标签下对于的变量获取对应comment下的data数据
                    commentGroup.prepend(tpl); //prepend是将数据放在容器的最前面，和append正好相反，append是放在容器的最后面。这里将最新评论放在最前面
                    textarea.val(''); // 评论后，将评论框种的字符串变成空的字符全，从而清除页面评论框的数据
                }else {
                    window.messageBox.showError(result['message']); // 如果返回的不是200，则通过messageBox展示错误信息
                }
            }
        });
    });
});