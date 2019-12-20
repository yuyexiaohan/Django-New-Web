
// 课程详情页js
$(function () {
    var span = $(".video-container span");
    var video_url = span.attr("data-video-url");
    var cover_url = span.attr("data-cover-url");
    var course_id = span.attr('data-course-id');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: video_url,
        image: cover_url,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        // primary: "flash", // 使用flash播放
        tokenEncrypt: "true",
        // AccessKey
        ak: 'f9ad7889318a4f5cb4d7d48223c2ca3e' // 注意保密
    });
    player.on("beforePlay",function (e) {
        if(!/m3u8/.test(e.file)){
            return;
        }

        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video_url': video_url,
                'course_id': course_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    player.setToken(e.file, token);
                    console.log("..start..",player.setToken(e.file,token));
                }else {
                    window.messageBox.showError(result['message']);
                    player.stop();
                }
            }
        });
    });
});