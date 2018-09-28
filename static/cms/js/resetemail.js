$(function(){
    $("#resetPwdBtn").click(function(ev){
        self=$(this)
        ev.preventDefault()
        checkcode=$("#exampleInputPassword3").val();
        email=$("#exampleInputPassword1").val();
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/send_checkcode/",
            type:"post",
            data:{
                "email":email,
                "checkcode":checkcode,
                "csrf_token":csrf_token
            },
            success:function(data){
                if(data.code==200)
                {
                    xtalert.alertSuccess(data.data)
                    self.attr("disabled",true)
                    var time=6;
                    self.html(time+"s")
                    var Timer=setInterval(function(){
                        self.html(--time+"s")
                        if(time<0)
                        {
                            clearInterval(Timer);
                            self.html("获取验证码")
                            self.attr("disabled",false)
                        }
                    },1000)
                }
                else{
                    xtalert.alertError(data.data)
                }

            }
        })

    })
})


$(function(){
    $("#resetPwdBtn1").click(function(ev){
        ev.preventDefault();
        email=$("#exampleInputPassword1").val();
        checkcode=$("#exampleInputPassword3").val();
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/resetemail/",
            type:"post",
            data:{
                "email":email,
                "checkcode":checkcode,
                "csrf_token":csrf_token
            },
            success:function(data){
                if(data.code==200)
                {
                    xtalert.alertSuccess(data.data)
                }
                else{
                    xtalert.alertError(data.data)
                }

            }
        })

    })
})