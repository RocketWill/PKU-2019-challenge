;
var url_detect_ops = {
    init: function () {
        this.eventBind();
        this.resizeContent();
    },

    eventBind: function () {
        var that = this;
        $(".url_detect_wrap .submit").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disable")) {
                alert("正在處理，請勿重複提交");
                return;
            }

            var url_input = $("#url_input").val();
            //console.log(url_input);
            if (url_input == null || url_input.length<3){
                alert("请输入大于3个字符的内容");
                return false;
            }

            $.ajax({
                url:'/url-detect',
                type:"POST",
                data:{"url":url_input},
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disable");
                    var callback = null;
                    if (res.code == 200) {
                        window.location.href = res.link;
                    }
                    else{
                        alert(res.msg);
                    }

                }
            });
        })
    },

    resizeContent: function() {
        $height = $(window).height() - 250;
        $('#page-frame').height($height);
    }
};


$(document).ready(function () {

    url_detect_ops.init();
    $(window).resize(function () {
        url_detect_ops.resizeContent();
    });

});

