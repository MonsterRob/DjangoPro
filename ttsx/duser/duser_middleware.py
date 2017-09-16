from django.utils.deprecation import MiddlewareMixin


class URLMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path not in ['/user/login/',
                                '/user/register/',
                                '/user/check_login/',
                                '/user/register_in/',
                                '/user/check_name/',
                                '/user/logout/'
                                ]:
            request.session['url_path'] = request.get_full_path()
