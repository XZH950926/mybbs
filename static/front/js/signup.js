$(function () {
    $("#send_sms_code_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val()
        csrf_token = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        $.ajax({
            url:'/send_sms_code/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf_token
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("发送短信验证码成功")
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
    $(".captcha").click(function(ev){
        ev.preventDefault();
        var r=Math.random();
        self=$(this)
        url=self.attr("data-src")+"?a="+r
        self.attr("src",url)
    })
     $("#signup_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        smscode = $('input[name=smscode]').val();
        username = $('input[name=username]').val();
        password = $('input[name=password]').val();
        password1 = $('input[name=password1]').val();
        captchacode = $('input[name=captchacode]').val();
        location=$("meta[name=location]").attr("value");

        ev.preventDefault();
        $.ajax({
            url:'/signup/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'smscode':smscode,
                'username':username,
                'password':password,
                'password1':password1,
                'captchacode':captchacode
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast(data.data);
                    window.location.href=location
                } else {
                    xtalert.alertErrorToast(data.data);
                }
            }
        })
    })
})

