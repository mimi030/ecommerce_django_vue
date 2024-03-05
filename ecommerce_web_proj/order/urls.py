from django.urls import path
from order import views


urlpatterns = [
    path('checkout/', views.checkout, name='post_checkout'),
    path('orders/', views.OrdersList.as_view()),
]
