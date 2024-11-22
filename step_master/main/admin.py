from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage
from .models import Order 

def image_show(self, obj):
    """Метод для отображения изображения в админке"""
    if obj.image:
        return mark_safe(f"<img src='{obj.image.url}' width='60' />")
    return "Нет изображения"

image_show.__name__ = "Изображение"  # Устанавливаем имя для метода отображения


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  # Указываем, сколько дополнительных изображений будет выводиться
    max_num = 2  # Максимальное количество дополнительных изображений на одну модель

    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    # Используем общую функцию image_show
    def image_show(self, obj):
        return image_show(self, obj)  # Вызов глобальной функции


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_show']

    # Используем общую функцию image_show
    def image_show(self, obj):
        return image_show(self, obj)  # Вызов глобальной функции
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'created_at')  # Поля для отображения в списке
    list_filter = ('created_at',)  # Добавляет фильтрацию по дате создания
    search_fields = ('name', 'email', 'phone')  # Поиск по имени, email и телефону
    ordering = ('-created_at',)  # Сортировка: сначала новые заказы
