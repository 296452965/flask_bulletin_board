// 自定义回调函数
// 分页按钮动态激活
// $ (function(){/*...*/});是$(document).ready(function(){/*...*/})的简写形式，是在DOM加载完成后执行的回调函数，并且只会执行一次。
$(function(){
    console.log('here');
    $(".pagination").find("li").each(function () {
        const a = $(this).find("a:first")[0];
        if ($(a).attr("href") === location.pathname+location.search) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
});

// 日期选择器
$(function(){
    // 输入最初为空
    $('input[name="datefilter"]').daterangepicker({
        autoUpdateInput: false,
        locale: {
            cancelLabel: '清空'
        }
    });

    $('input[name="datefilter"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
    });

    $('input[name="datefilter"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });

});

// 侧边栏动态激活方式一，通过当前url判断
$(function () {
    $(".sidebar-main").find("li").each(function () {
        const a = $(this).find("a:first")[0];
        if ($(a).attr("href") === location.pathname) {
            $(this).parents("li").addClass("open");
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
});

// 侧边栏动态激活方式二，需要给标签加id
// var url_array = document.location.pathname.split("/");
// s1 = url_array[1];
// s2 = url_array[2];
// if (s1 === ''){
//     $('#index').addClass('active')
// } else {
//     $("#"+s1).addClass('open');
//     $("#"+s2).addClass('active')
// };