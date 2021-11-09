from django.urls import path, include
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('product/<int:product_id>/', views.product_info, name='product_info'),
    path('reg', views.reg, name='reg'),
    path('auth', views.auth, name='auth'),
    path('category/<int:id_category>/', views.category, name='category'),
    path('basket_adding/', views.basket_adding, name='basket_adding'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart')
]
