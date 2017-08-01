/**
 * Created by wzz on 2017/8/1.
 */
$(function () {
    var error_name = false;
    var error_password = false;

    $('#user_name').blur(function () {
        check_user_name();
    });
    $('#user_pwd').blur(function () {
        check_pwd();
    });

    function check_user_name() {
        var user_name = $('#user_name').val();
        var len = user_name.length;
        if (len < 5 || len > 20) {
            $('#user_name').next().html('请输入5-20个字符的用户名')
            $('#user_name').next().show();
            error_name = true;
        }
        else {
            $.get('/user/check_name/',{'uname':user_name}, function (data) {
                if (!data['result']){
                    // 数据库有数据
                    $('#user_name').next().html('用户名不存在');
			        $('#user_name').next().show();
			        error_name = true;
			        return false;
                }
            });
            $('#user_name').next().hide();
            error_name = false;

        }
    }

    function check_pwd() {
        var len = $('#user_pwd').val().length;
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位');
            $('#pwd').next().show();
            error_password = true;
        }
        else {

            $('#pwd').next().hide();
            error_password = false;
        }
    }


    $('#log_form').submit(function () {
        check_user_name();
        check_pwd();

        return !(error_name||error_password);
    });
});