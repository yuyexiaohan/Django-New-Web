/* 轮播图js配置文件 */


 // 定义一个函数给关闭按钮添加关闭事件,并将对应的数据库数据删除
 /*************************************/
// 不能加$符号，否则所有变量都是局部变量，不加该函数是全局变量
function addCloseBannerEvent(bannerItem) {
    var closeBtn = bannerItem.find('.close-btn'); //找到关闭按钮标签
    // 找到该变量被点击，执行事件
    var bannerId = bannerItem.attr('data-banner-id');
    closeBtn.click(function () {
        console.log('关闭按钮！');// 打印测试
        if(bannerId){
            // 需要弹出是否确认删除对话框
            xfzalert.alertConfirm({
                'text':'确定要删除这个轮播图吗？',
                'confirmCallback':function () {
                    xfzajax.post({
                        'url':'/cms/delete_banner/',
                        'data':{
                            'banner_id':bannerId
                        },
                        'success':function (result) {
                            if (result['code']===200){
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功！');
                            }else {
                                bannerItem.remove();
                            }
                        }
                    });
                }
            });
        }else{
            bannerItem.remove();
        }

    });
}
// /*************************************/


// 定义一个用来绑定选择图片的事件
 /*************************************/
function addImageSelectEvent(bannerItem) {
    var image = bannerItem.find('.banner-image'); // 获取图片标签
    var imageSlect = bannerItem.find('.image-select'); // 获取图片同级的隐藏input标签
    image.click(function () {
       // input[type='file'] 类型，才能够在网页上打开文件选择框
        // 处理方式可以将image标签中隐藏一个input标签，这样就可以直接在浏览器中打开文件上传框，上传文件（图片）
        // {# 加入一个input标签，并将style设置为display:none来隐藏标签 #}
        imageSlect.click(); // 点击input点击事件，弹出文件选择对话框
    });
        console.log('图片被点击');
    // 识别当input标签动作后，执行如下操作
    imageSlect.change(function () {
        var file = this.files[0]; // 拿到这个点击事件拿到的文件
        var formData = new FormData(); // 获取数据
        formData.append('upfile',file); // 其中将文件传到服务器时，名字"upfile"与视图函数定义一致
        console.log('图片准备上传服务器');
        xfzajax.post({
           'url':'/cms/upload_file/',
            'data':formData,
            'processData':false, // 注明传输的是一个文件不是一个字符串
            'contentType':false,
            'success':function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    console.log(url); // 打印url
                    image.attr('src',url);// 修改图片的属性，加入图片的url,这样图片添加后，就可以在网页上显示了
                } else {
                    console.log("code", result["code"]);
                }
            }
        });
        console.log('图片已上传'); // 测试用
    });
}
 /*************************************/

 // 添加保存轮播图事件
 /*************************************/
 function addSaveBannerEvent(bannerItem) {
     var saveBtn = bannerItem.find('.save-btn'); //获取保存标签
     var image = bannerItem.find('.banner-image');// 获取图片标签
     var priorityIput = bannerItem.find("input[name='priority']"); // 优先级
     var linktoInput = bannerItem.find("input[name='link_to']");
     var bannerId = bannerItem.attr('data-banner-id');
     var url = '';
     if (bannerId){
        url = '/cms/edit_banner/';
     }else {
         url = '/cms/add_banner/';
     }
     saveBtn.click(function () {
        var image_url = image.attr('src'); // 获取链接
         var priority = priorityIput.val();
         var link_to = linktoInput.val();
         xfzajax.post({
             'url':url,
             'data':{
                 'image_url':image_url,
                 'priority':priority,
                'link_to':link_to,
                 'pk':bannerId // 这边添加会经过视图函数，pk这个值在视图函数中不会获取，就不会影响数据库存储，不会产生相关报错等影响
             },
            'success':function (result) {
                if(result['code'] === 200){

                    if(!bannerId){
                        // var bannerId = result['data']['banner_id'];
                        // 这里如果在使用var bannerId=定义这个变量，就等价与重新定义这个变量。在js中var定义一个变量，函数实际执行时在函数名前将变量名以undefined形式先申明，之后再取值。这里如果使用var申明bannerId的话，if判断中的bannerId就没有定义这样运行程序就会报错。
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerId); // 获取这个轮播图的id
                        window.messageBox.showSuccess('轮播图添加成功！');
                    }else {
                        window.messageBox.showSuccess('轮播图修改成功！');
                    }
                    console.log('20000....');
                    var prioritySpan = bannerItem.find('.priority-span');
                    prioritySpan.text('优先级:'+priority);
                    location.reload();
                }
            }
         })
     });
 }
  /*************************************/


// 因为代码重复使用某些变量，所有这里创建一个函数包含共同的函数
/*************************************/
function createBannerItem(banner) {
    var tpl = template("banner-item",{'banner':banner}); //如果不传如banner则在html中有判断，会跳转到banner不存在的显示界面
    var bannerListGroup = $(".banner-list-group"); // 定义对应类别标签的变量
    var bannerItem = null;
    if(banner){
        bannerListGroup.append(tpl);//正序添加，最新添加的排在后面 // 将模板放在class="banner-list-group"的标签中去
        bannerItem = bannerListGroup.find('.banner-item:last');// 因为如果是appent正序添加，最新的就是找最后一个这里是与appent对应
    }else {
        bannerListGroup.prepend(tpl); // 倒序添加，最新添加的放在最前面
        // 当模板添加后，再在模板中添加需要的点击事件（例如：关闭，保存等）
        bannerItem = bannerListGroup.find('.banner-item:first');//因为如果是prepent倒序添加，最新的就是找第一个
    }
    addCloseBannerEvent(bannerItem);
    addImageSelectEvent(bannerItem);
    addSaveBannerEvent(bannerItem);
}
/*************************************/


// 网页加载完毕后就执行获取轮播图列表事件
/*************************************/
$(function () {
   xfzajax.get({
      'url':'/cms/banner_list/',
      'success':function (result) {
          if(result['code']=== 200){
              var banners = result['data']['banners']; // data是一个集合，需要使用banners获取数据
              for(var i=0; i<banners.length;i++){
                  var banner = banners[i];
                  createBannerItem(banner);
              }
          }
      }
   });
});


/*************************************/





//定义一个添加轮播图事件：
// 调用轮播图模板文件（现在html文件中编写一个静态文件，然后使用art_temple作为模板文件添加到对应的html标签中去）
 /*************************************/
$(function () {
    var addBtn = $('#add-banner-btn');
    var bannerListGroup = $(".banner-list-group");
    addBtn.click(function () {
        // 如果有点击事件，就获取模板（art_temple）文件.在HTML文件种一般是放在一个script标签种然后使用{%verbatim %}和{%endverbatim %}标签包裹
        var length = bannerListGroup.children().length; // bannerListGroup的子类就是轮播图，借此统计轮播图数量
        if(length >= 6 ){
            window.messageBox.showInfo('最多只能添加6张轮播图！')
        }else{
            createBannerItem();
        }
    });
});
 /*************************************/



