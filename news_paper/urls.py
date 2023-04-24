from django.urls import path
from .views import (
PostList, PostDetail, PostCreate, PostUpdate, PostDelete, subscriptions
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(300)(PostList.as_view()), name ='post_list'),
    path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),

]