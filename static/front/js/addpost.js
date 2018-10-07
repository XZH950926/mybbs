$(function () {
     var ue = UE.getEditor("editor",{
         'serverUrl': '/upload/'
     });

     $('#addpost').click(function (ev) {
         ev.preventDefault();
         var title = $('input[name=postname]');
         var boarder_id = $('select[name=boarderid]');
         var content = ue.getContent();
         var csrf_token=$("meta[name=csrf_token]").attr("value")
        $.ajax({
            url:'/addpost/',
            type:'post',
            data:{
                'title':title.val(),
                'border_id':boarder_id.val(),
                "csrf_token":csrf_token,
                'content':content
            },
            success:function (data) {
                xtalert.alertSuccessToast("发帖成功");
                window.location.href = '/'
            }
        })
     })
})

