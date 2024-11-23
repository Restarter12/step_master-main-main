from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage
from .models import Order 

def image_show(self, obj):
    """Метод для отображения изображения в админке"""
    if obj.image:
        return mark_safe(f"<img src='{obj.image.url}' width='60' />")
    return "Нет изображения"

image_show.__name__ = "Изображение" 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Доп фото
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2 
    max_num = 2  


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


    def image_show(self, obj):
        return image_show(self, obj) 


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_show']
    def image_show(self, obj):
        return image_show(self, obj)  
    
# Создание формы в админке
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'total_price', 'display_products', 'created_at')
    
    def display_products(self, obj):
        return obj.products

    display_products.short_description = "Товары"
    class Meta:
        permissions = [
            ("can_place_order", "Can place order"),
        ]


