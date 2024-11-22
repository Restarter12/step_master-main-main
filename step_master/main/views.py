from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from .forms import OrderForm

# Функция для отображения списка товаров с фильтрацией по категориям
def product_list(request):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('categories')  # Список выбранных категорий
    products = Product.objects.filter(available=True)

    # Фильтруем товары по выбранным категориям
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    return render(request, 'main/tovar.html', {
        'categories': categories,
        'products': products
    })


# Функция для главной страницы
def index(request):
    # Выбираем товары для отображения (например, первые 8 товаров по дате создания)
    popular_products = Product.objects.filter(available=True).order_by('-created')[:8]
    return render(request, 'main/index.html', {'popular_products': popular_products})

def akses(request):
    return render(request, 'main/akses.html')

# Функция для страницы "О нас"
def about(request):
    return render(request, 'main/about.html')

# Функция для страницы товаров
def tovar(request):
    return render(request, 'main/tovar.html')


# Функция для отображения деталей товара
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)  # Получаем товар по id и slug
    cart_product_form = CartAddProductForm()  # Создаем форму добавления товара в корзину
    return render(request, 'main/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })


def submit_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение данных в базу
            return redirect('success')  # Укажите страницу после успешной отправки
    else:
        form = OrderForm()

    return render(request, 'main/layout.html', {'form': form})

def success(request):
    return render(request, 'main/success.html')