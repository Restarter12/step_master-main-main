from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import OrderForm
from cart.cart import Cart
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Отображение списка товаров с фильтрацией по категориям
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

# Отправка заказа
def submit_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total_price()
            order.products = ", ".join([f"{item['product']} (x{item['quantity']})" for item in cart])
            order.save()
            cart.clear()
            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('success')
    else:
        form = OrderForm()
    return render(request, 'main/submit_order.html', {'form': form})

# Страница успешного заказа
def success(request):
    return render(request, 'main/success.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')


@login_required
def place_order(request):
    if request.method == 'POST':
        # Логика оформления заказа
        return redirect('success_page')  # Перенаправление на страницу успешного оформления
    return render(request, 'order_form.html')


