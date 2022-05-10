'''

商品页面静态化

'''



#让该脚本可单独运行
import sys

#../ 表示当前目录的上一级目录
sys.path.insert(0, '../')


# 告诉django配置文件在哪儿
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopping_mall.settings")


import django
django.setup()




from apps.goods.models import SKU
from utils.goods import get_categories,get_breadcrumb,get_goods_specs

def generic_detail_html(sku):
    # try:
    #     sku = SKU.objects.get(id=sku_id)
    # except Exception as e:
    #     return JsonResponse({'code': 0, 'errmsg': '错误'})

    categories = get_categories()

    breadcrumb = get_breadcrumb(sku.category)
    goods_specs = get_goods_specs(sku)

    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs
    }

    from django.template import loader
    detail_temple = loader.get_template('detail.html')
    detail_html_data = detail_temple.render(context)


    import os
    from shopping_mall import settings
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR),'front_end_pc/goods/%s.html'%sku.id)

    with open(file_path,'w',encoding='utf-8') as f:
        f.write(detail_html_data)




skus = SKU.objects.all()
for sku in skus:
    generic_detail_html(sku)