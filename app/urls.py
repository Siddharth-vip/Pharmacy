from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.register, name='register'),
    path('users/login/', views.user_login, name='login'),
    path('users/logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('users/edit_profile/',views.edit_profile,name='edit_profile'),
    path('users/help_support/',views.help_support,name='help_support'),
    path('users/about/',views.about,name='about'),
    path('users/contact/',views.contact,name='contact'),
    path('products/',views.products, name='products'),
    path('products/<uuid:id>',views.product, name='product'),
    path('cart/',views.cart,name="cart"),
    path('add_item/<uuid:id>/',views.add_item,name='add_item'),
    path('remove_item/<uuid:id>/',views.remove_item,name='remove_item'),
    path('add_to_cart/<uuid:id>/',views.add_to_cart,name='add_to_cart'),
    path('search/', views.search_products, name='search_products'),
    path('buy_now/',views.buy_now,name="buy_now")
]
