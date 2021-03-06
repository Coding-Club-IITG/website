from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.product_list, name='product-home'),
    path('s/', views.search, name='search'),
    path('', views.product_list, name='product_list'),
    path('manageproducts/', views.manage_products, name='manageproducts'),
    re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]
