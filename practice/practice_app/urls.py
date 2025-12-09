from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
    path('checkout/', views.checkout, name='checkout'),
    path('receipt/<int:sale_id>/', views.receipt, name='receipt'),
    path('add_all_to_cart/', views.add_all_to_cart, name='add_all_to_cart'),

]
