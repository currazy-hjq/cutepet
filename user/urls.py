from django.conf.urls import url

from user import views

urlpatterns = [
    # http://127.0.0.1:8000/v1/users/
    url(r'^$', views.Users.as_view()),
    # http://127.0.0.1:8000/v1/users/activation?code=xxxxx
    url(r'^activation$',views.user_active),
]