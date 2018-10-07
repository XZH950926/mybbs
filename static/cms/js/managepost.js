$(function(){
    $(".update-btn").click(function(ev){
        ev.preventDefault();
        self=$(this)
        var data_tag=self.attr("data-tag")
        csrf_token=$("meta[name=csrf_token]").attr("value")
        url="/cms/jiajin/"
        if(data_tag=="canceltag")
        {
            url="/cms/canel/"
        }

         data_id=self.attr("data-id")
        $.ajax({
            url:url,
            type:"post",
            data:{
                "csrf_token":csrf_token,
                "data_id":data_id
            },
            success:function(data){
                if(data.code==200)
                {
                    xtalert.alertSuccessToast("加精成功")
                    window.location.reload()
                }
                else{
                    xtalert.alertErrorToast("加精失败")
                }
            }
        })


    })
})