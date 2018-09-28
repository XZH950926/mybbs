$(function () {
    $("#pwd_sms_code_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val()
        csrf_token = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        $.ajax({
            url: '/change_pwd_sms/',
            type: 'post',
            data: {
                'telephone': telephone,
                'csrf_token': csrf_token
            },
            success: function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast(data.data)
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.data)
                }
            }
        })
    })


   $("#signup_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        smscode = $('input[name=smscode]').val();
        password = $('input[name=password]').val();
        password1 = $('input[name=password1]').val();

        ev.preventDefault();
        $.ajax({
            url:'/findpwd/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                "smscode":smscode,
                'password':password,
                'password1':password1,
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast(data.data);
                    window.location.href="/signin/"
                } else {
                    xtalert.alertErrorToast(data.data);
                }
            }
        })
    })

})