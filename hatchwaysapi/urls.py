from django.conf.urls import url, include
from . import views
from django.urls import path



urlpatterns = [
    path('api/ping', views.ping),
    # path('api/posts',views.posts),
    path('api/getyoutubedata',views.getYoutubeData),
    path('api/search',views.search)

]
