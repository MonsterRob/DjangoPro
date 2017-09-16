from haystack import indexes
from .models import Goodsinfo


# 指定对于某个类的某些数据建立索引
class GoodsinfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Goodsinfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
