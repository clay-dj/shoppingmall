from django.views import View
from utils.goods import get_categories
from django.shortcuts import render
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categories()

        # 渲染模板的上下文
        context = {
            'categories': categories,

        }
# Create your views here.
