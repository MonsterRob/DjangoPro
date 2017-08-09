from django.template import Library

register = Library()


@register.filter
def my_index(ls, index_):
    return ls[index_]


@register.filter
def my_mul(var1, var2):
    return var1 * var2


@register.filter
def my_len(ls):
    return len(ls)
