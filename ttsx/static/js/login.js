/**
 * Created by wzz on 2017/8/1.
 */
$(function () {
    var error_name = false;

    $('#user_name').blur(function() {
		check_user_name();
	});

	function check_user_name(){
        var user_name = $('#user_name').val();
		var len = user_name.length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名')
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
		    $.get('/user/check_name/',{'uname':user_name}, function (data) {
                if (data['result']){
                    // 数据库有数据
                    $('#user_name').next().html('此用户名已被注册')
			        $('#user_name').next().show();
			        error_name = true;
			        return false;
                }
            });

			$('#user_name').next().hide();
			error_name = false;

		}
	}
});