from apps.goods.views import IndexView,ListView,SKUSearchView,DatailView,CategoryVisitCountView
from django.urls import path

urlpatterns = [
    path('index/',IndexView.as_view()),
    path('search/',SKUSearchView()),#SKUSearchView继承自SearchView没有as_view方法
    path('list/<category_id>/skus/',ListView.as_view()),
    path('detail/<sku_id>/',DatailView.as_view()),
    path('detail/visit/<category_id>/', CategoryVisitCountView.as_view()),

]