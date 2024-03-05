from django.urls import path, include
from product import views

urlpatterns = [
    # path('latest-products/', views.LatestProductList.as_view()),
    path('latest-products/', views.LatestProductList.as_view(), name='get_post_products'),
    path('products/search/', views.search),
    # path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view(), name='get_delete_update_product'),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]
