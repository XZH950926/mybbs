$(function(){
    $("#saveBorder").click(function (ev) {
        ev.preventDefault();
        borderName=$("#borderName").val();
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/addborder/",
            type:"post",
            data:{
                "borderName":borderName,
                "csrf_token":csrf_token
            },
            success:function(data){
                if (data.code=200)
                {
                     xtalert.alertSuccessToast(data.data)
                    setTimeout(function(){
                    window.location.reload()
                    },2000)
                }
                else{
                    xtalert.alertErrorToast(data.data)
                }
            }
        })

    })
$(".delete-btn").click(function(ev){
    self=$(this);
     ev.preventDefault();
        id=self.attr("data-id")
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/deleteborder/",
            type:"post",
            data:{
                "id":id,
                "csrf_token":csrf_token
            },
            success:function(data){
                if (data.code=200)
                {
                     xtalert.alertSuccessToast(data.data)
                    setTimeout(function(){
                    window.location.reload()
                    },2000)
                }
                else{
                    xtalert.alertErrorToast(data.data)
                }
            }
        })
})

$(".update-btn").click(function(){
    self=$(this)
    $("#borderName1").val(self.attr("data-borderName"))
    $("#create_time").val(self.attr("data-create_time"))
    $("#saveBorder1").attr("fromdata",self.attr("data-id"))
})



    $("#saveBorder1").click(function (ev) {
        ev.preventDefault();
        self=$(this)
        id=self.attr("fromdata")
        borderName=$("#borderName1").val();
        create_time=$("#create_time").val();
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/updateborder/",
            type:"post",
            data:{
                "id":id,
                "create_time":create_time,
                "borderName":borderName,
                "csrf_token":csrf_token
            },
            success:function(data){
                if (data.code=200)
                {
                     xtalert.alertSuccessToast(data.data)
                    setTimeout(function(){
                    window.location.reload()
                    },2000)
                }
                else{
                    xtalert.alertErrorToast(data.data)
                }
            }
        })

    })

})
