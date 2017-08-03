from django.template import Library

register = Library()


@register.filter
def my_index(ls, index_):
    return ls[index_]
