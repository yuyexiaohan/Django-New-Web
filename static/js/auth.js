/* auth的注册功能部分 */

//实现图片验证码自动更新功能
//原理：设置功能每次获取imaCapacha函数刷新一次就会产生一个新的图形验证码。
// 这里利用src标签的内容一旦更改，图形验证码就会更新的原理。
// 使用JS写一个函数利用account/img_captcha/随机数的方式进行更新路由，产生新的验证码
$(function () {
    var imgCaptcha = $('.img-captcha');
   console.log('点击刷新图形验证码...');
    imgCaptcha.click(function () {
        // alert('11111');
        imgCaptcha.attr("src",'/account/img_captcha/'+"?random="+Math.random());
    });
});

// 点击发送短信验证码
$(function () {
    var smsCaptcha = $('.sms-captcha-btn');
    function send_sms() {
        // var telephone = $('input[name="telephone"]');
        console.log('测试...');
        var telephone = $('input[name="telephone"]').val();
        // var telephone=document.getElementById("test");
        $.get({
            'url': '/account/sms_captcha/',
            // 'telephone': telephone,
            'data':{'telephone':telephone},
            'success': function (result) {
                var count = 20; // 短信验证码倒计时时间定义
                smsCaptcha.addClass('disabled');
                smsCaptcha.unbind('click');
                var timer = setInterval(function () {
                    smsCaptcha.text(count);
                    count--;
                    if (count <= 0){
                        clearInterval(timer);
                        smsCaptcha.text('发送验证码');
                        smsCaptcha.removeClass('disabled');
                        smsCaptcha.click(send_sms);
                    }
                },1000)
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    }
    smsCaptcha.click(send_sms);
    // smsCaptcha.click(function () {
    //     var telephone = $('input[name="telephone"]');
    //     // var telephone = $('input[name="telephone"]').val();
    //     // var telephone=document.getElementById("test");
    //     $.get({
    //         'url': '/account/sms_captcha/',
    //         'telephone': telephone,
    //         'success': function (result) {
    //             console.log('短信发送成功！');
    //             var count = 10;
    //             smsCaptcha.addClass('disabled');
    //             var timer = setInterval(function () {
    //                 smsCaptcha.text(count);
    //                 count--;
    //                 if (count <= 0){
    //                     clearInterval(timer);
    //                     smsCaptcha.text('发送验证码');
    //                     smsCaptcha.removeClass('disabled');
    //                 }
    //             },1000)
    //         },
    //         'fail': function (error) {
    //             console.log(error);
    //         }
    //     });
    // });
});

// 注册功能
$(function () {
    var telephoneInput = $("input[name='telephone']");
    var usernameInput = $("input[name='username']");
    var imgCaptchaInput = $("input[name='img_captcha']");
    var password1Input = $("input[name='password1']");
    var password2Input = $("input[name='password2']");
    var smsCaptchaInput = $("input[name='sms_captcha']");
    var submitBtn = $(".submit-btn");

    submitBtn.click(function (event) {
        // 禁止掉传统表单发送数据的方式，因为使用表单形式的时候点击‘注册’
        // 会将信息通过表单提报给数据库，但是现在我们使用ajax的方式传输数据，
        // 如果不阻止的话，当点击‘注册’时，后台还是会以传统表单的形式传送数据
        event.preventDefault();
        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var imgcaptcha = imgCaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var smscaptcha = smsCaptchaInput.val();

        if(!telephone || telephone.length != 11){
            alert('手机号码输入不正确！');
            return;
        }

        xfzajax.post({
            'url': '/account/register/',
            'data':{
                'telephone':telephone,
                'username':username,
                'img_captcha':imgcaptcha,
                'password1':password1,
                'password2':password2,
                'sms_captcha':smscaptcha
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.location = '/';
                }else{
                    //使用message文件的方式将所有错误信息进行返回,相比直接使用js的alert会好看实用写
                    var message = result['message'];
                    window.messageBox.showError(message);
                    // 使用js自带的弹框alert
                    // alert(result['message']);
                }
            },
            'fail':function (error) {
                console.log(error);
            }
        });
    });

});
