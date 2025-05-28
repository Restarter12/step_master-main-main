from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import contact_view
urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('tovar/', views.product_list, name="tovar"),  # Изменен путь для отображения товаров
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),  # Для фильтрации по категориям
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),  # Путь для деталей товара
    path('submit_order/', views.submit_order, name='submit_order'),
    path('success/', views.success, name='success'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path("contact/", contact_view, name="contact"),
]
