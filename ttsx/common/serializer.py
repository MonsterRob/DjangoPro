from rest_framework import serializers

from .models import Goodsinfo, TypeInfo


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goodsinfo
        fields = ['id', 'gtitle', 'gpic',
                  'gprice', 'gunit'
                  ]
