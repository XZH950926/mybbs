$(function(){
    $("#saveBanner").click(function(ev){
        ev.preventDefault();
        csrf_token=$("meta[name=csrf_token]").attr("value");
        bannerName=$("#bannerName").val();
        imglink=$("#imglink").val();
        link=$("#link").val();
        priority=$("#priority").val();
        $.ajax({
            url:"/cms/addbanner/",
            type:"post",
            data:{
                "csrf_token":csrf_token,
                "bannerName":bannerName,
                "imglink":imglink,
                "link":link,
                "priority":priority
            },
            success:function(data){
                if(data.code==200)
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
        ev.preventDefault();
        self=$(this)
        id=self.attr("data-id")
        csrf_token=$("meta[name=csrf_token]").attr("value");
        $.ajax({
            url:"/cms/deletebanner/",
            type:"post",
            data:{
                "id":id,
                "csrf_token":csrf_token
            },
            success:function(data){
                if (data.code==200)
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


    $(".update-btn").click(function(ev){
       ev.preventDefault();
       self=$(this)
        $("#bannerName1").val(self.attr("data-bannerName"));
        $("#imglink1").val(self.attr("data-imglink"));
        $("#link1").val(self.attr("data-link"));
        $("#priority1").val(self.attr("data-priority"))
        $("#saveBanner1").attr("fromdata",self.attr("data-id"))
    })


 $("#saveBanner1").click(function(ev){
        ev.preventDefault();
        self=$(this)
        csrf_token=$("meta[name=csrf_token]").attr("value");
        id=self.attr("fromdata")
        bannerName=$("#bannerName1").val();
        imglink=$("#imglink1").val();
        link=$("#link1").val();
        priority=$("#priority1").val();
        $.ajax({
            url:"/cms/updatebanner/",
            type:"post",
            data:{
                "csrf_token":csrf_token,
                "id":id,
                "bannerName":bannerName,
                "imglink":imglink,
                "link":link,
                "priority":priority
            },
            success:function(data){
                if(data.code==200)
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

    // 上传图片到七牛云
uploader = Qiniu.uploader({
            runtimes: 'html5,html4,flash',
            browse_button: 'select_img_btn',//上传按钮的ID,
            max_file_size: '4mb',//最大文件限制
            dragdrop: false, //是否开启拖拽上传
            uptoken_url: '/common/qiniu_token/',//设置请求qiniu-token的url
            domain: 'pfpjd7i5o.bkt.clouddn.com',//自己的七牛云存储空间域名
            get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
            auto_start: true, //如果设置了true,只要选择了图片,就会自动上传
            unique_names: true,
            multi_selection: false,//是否允许同时选择多文件
            //文件类型过滤，这里限制为图片类型
            filters: {
              mime_types : [
                {title : "Image files", extensions: "jpg,jpeg,png"}
              ]
            },
            init: {
                'FileUploaded': function(up, file, info) {
                   var res = eval('(' + info + ')');
                    res.key;//获取上传文件的链接地址
                   // $('#imglink').attr('value',sourceLink)
                    sourceLink = 'http://pfpjd7i5o.bkt.clouddn.com/' + res.key;
                    console.log(sourceLink)  // 访问图片的网址
                    // 放到我们的input标签中
                    $("#imglink").val(sourceLink);
                },
                'Error': function(up, err, errTip) {
                    console.log(err);
                    xtalert.alertErrorToast("上传失败")
                }
            }
        })

})