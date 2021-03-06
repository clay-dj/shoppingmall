from django.shortcuts import render
from django.views import View
from utils.goods import get_categories, get_breadcrumb, get_goods_specs
from collections import OrderedDict
from apps.contents.models import ContentCategory
from apps.goods.models import GoodsChannel, GoodsCategory
from django.http import JsonResponse
from apps.goods.models import SKU


class IndexView(View):
    def get(self, request):
        categories = get_categories()
        # 2.广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

            # 我们的首页 后边会讲解页面静态化
            # 我们把数据 传递 给 模板
        context = {
            'categories': categories,
            'contents': contents,
        }
        # 模板使用比较少，以后大家到公司 自然就会了
        return render(request, 'index.html', context)


# 商品列表功能和排序功能
class ListView(View):
    def get(self, request, category_id):
        # 1.接收参数
        # 排序字段
        ordering = request.GET.get('ordering')
        # 每页多少条数据
        page_size = request.GET.get('page_size')
        # 要第几页数据
        page = request.GET.get('page')

        # 2.获取分类id
        # 3.根据分类id进行分类数据的查询验证
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4.获取面包屑数据
        breadcrumb = get_breadcrumb(category)

        # 5.查询分类对应的sku数据，然后排序，然后分页
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        # 分页
        from django.core.paginator import Paginator
        # object_list, per_page
        # object_list   列表数据
        # per_page      每页多少条数据
        paginator = Paginator(skus, per_page=page_size)

        # 获取指定页码的数据
        page_skus = paginator.page(page)

        sku_list = []
        # 将对象转换为字典数据
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 获取总页码
        total_num = paginator.num_pages

        # 6.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'list': sku_list, 'count': total_num, 'breadcrumb': breadcrumb})


from django.http import JsonResponse
from haystack.views import SearchView

'''
SearchView中有一个creat_response方法 返回的不是json数据，
所以我们要从写这个方法让其返回json数据



'''


class SKUSearchView(SearchView):
    def create_response(self):
        context = self.get_context()
        # get_context()方法获取搜索结果
        sku_list = []
        for sku in context['page'].object_list:
            sku_list.append({
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })

        return JsonResponse(sku_list, safe=False)


class DatailView(View):
    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'code': 0, 'errmsg': '错误'})

        categories = get_categories()

        breadcrumb = get_breadcrumb()
        goods_specs = get_goods_specs(sku)

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs
        }

        return render(request, 'detail.html', context)


class CategoryVisitCountView(View):
    def post(self, request, category_id):

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        from datetime import date

        today_date = date.today()

        from apps.goods.models import GoodsVisitCount

        try:
            gvc = GoodsVisitCount.objects.get(category=category, date=today_date)
        except GoodsVisitCount.DoesNotExist:
            # 4. 没有新建数据
            GoodsVisitCount.objects.create(category=category,
                                           date=today_date,
                                           count=1)
        else:
            # 5. 有的话更新数据
            gvc.count += 1
            gvc.save()
            # 6. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


