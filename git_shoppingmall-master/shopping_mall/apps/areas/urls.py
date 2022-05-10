from django.conf.urls import url
from django.urls import path
from apps.areas.views import AreasView,SubAreaView

from . import views
urlpatterns = [
    path('areas/',AreasView.as_view()),
    path('areas/<id>/',SubAreaView.as_view()),
]