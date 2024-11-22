from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('tovar/', views.product_list, name="tovar"),  # Изменен путь для отображения товаров
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),  # Для фильтрации по категориям
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),  # Путь для деталей товара
    path('submit_order/', views.submit_order, name='submit_order'),
    path('success/', views.success, name='success'), 
    path('akses/', views.akses, name="akses")
]
