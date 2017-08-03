from django.contrib import admin
from .models import Goodsinfo, TypeInfo


# Register your models here.
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle', 'gprice', 'gclick', 'gkucun', 'gtype']
    list_per_page = 15


admin.site.register(TypeInfo)
admin.site.register(Goodsinfo, GoodsAdmin)
