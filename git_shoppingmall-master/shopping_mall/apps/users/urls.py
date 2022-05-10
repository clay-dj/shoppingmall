from django.urls import path

from apps.users.views import RegisterView,UsernameCountView,LoginView,CenterView,EmailView
from apps.users.views import EmailVerifyView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('username/<username:username>/count/',UsernameCountView.as_view()),
    path('login/',LoginView.as_view()),
    path('info/',CenterView.as_view()),
    # path('emails/ ',EmailView.as_view()),
    path('emails/',EmailView.as_view()),
    path('emails/verification/',EmailVerifyView.as_view()),
]