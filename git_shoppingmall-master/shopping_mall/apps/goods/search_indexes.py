from haystack import indexes
from apps.goods.models import SKU
'''
1.需要在对应的子应用中 创建search_indexes.py 文件，该文件名字必须为search_indexes
2.索引类必须继承indexes.SearchIndex和indexes.Indexable类
3.必须定义一个子段 dacument = True
4.在单独的文件夹下创建search/indexes/子应用名/模型类小写_text.txt文件


haystack 获取数据传给es


在虚拟环境下运行python manage.py  rebulid_index


'''

class SkuIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return SKU

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        # return SKU.object.all()

###查询,借用haystack调用es
