// 自定义函数
// 二级单位下拉列表联动响应
function change_unit_field(choose, target, url) {
    $("#unit-div").html('');
    let level_data;
    level_data = {
        'level': choose
    };
    $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify(level_data),
        contentType: "application/json; charset=UTF-8",
        success: function (data){
            if(data){
                if(choose===1){
                    $("<select class='form-control' name='unit' id='unit'></select>").appendTo("#"+target);
                    $("<option selected='selected' disabled='disabled'  style='display: none' value=''>请选择一级单位</option>").appendTo("#unit");
                    for(i=0;i<data.length;i++){
                        $("<option value='"+data[i].id+"'>"+data[i].unit_name+"</option>").appendTo("#unit")
                    }
                } else if(choose===2){
                    console.log('target',target);
                    console.log($('#'+target));
                    $("<select class='form-control' name='unit2' id='unit2'></select>").appendTo("#"+target);
                    $("<option selected='selected' disabled='disabled'  style='display: none' value=''>请选择二级单位</option>").appendTo("#unit2");
                    for(i=0;i<data.length;i++){
                        $("<option value='"+data[i].id+"'>"+data[i].unit_name+"</option>").appendTo("#unit2")
                    }
                }
            } else {
                alert('error')
            }
        }
    })
};
// 二级分类下拉列表联动响应
function change_field(choose,target,url) {
    console.log(choose);
    let c1data;
    const select = document.getElementById(choose);
    $("#"+target).html('');//每次重新选择当前列表框，就清空下一级列表框。
    for (let i = 0; i < select.length; i++) {
        if (select[i].selected) { //判断被选中项
            let c1id = select[i].value;
            c1data = {
                "c1id": c1id
            };
            $.ajax({//发起ajax请求
                url : url,
                type : "POST",
                data : JSON.stringify(c1data),
                contentType : "application/json; charset=UTF-8",
                success : function (data) {
                    if(data){
                        $("<option selected='selected' disabled='disabled'  style='display: none' value=''>请选择二级分类</option>").appendTo("#"+target);
                        for(i=0;i<data.length;i++){
                            $("<option value='"+data[i].id+"'>"+data[i].category+"</option>").appendTo("#"+target)
                        }
                    } else {
                        alert('error')
                    }
                }
            })
        }
    }
};
// 打开图片浏览模态框相关动作
$('#picModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const caseId = button.data('case-id');
    const picGetUrl = button.data('url');
    let pmdata = {
        'case_id':caseId
    };
    $.ajax({
        url:picGetUrl,
        type:'POST',
        data: JSON.stringify(pmdata),
        contentType : "application/json; charset=UTF-8",
        success : function (data) {
            if(data){
                $('.carousel-inner').html('');
                for(i=0;i<data.length;i++){
                    let picURL = "/admin/document/"+data[i];
                    if(i==0){
                        $("<div class='item active'><img src='"+picURL+"' height='464px' ></div>").appendTo($('.carousel-inner'))
                    }else{
                        $("<div class='item'><img src='"+picURL+"' height='464px' ></div>").appendTo($('.carousel-inner'))
                    }
                }
            } else {
                alert('error')
            }
        }
    });

    })