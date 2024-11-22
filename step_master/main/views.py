from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import OrderForm
from cart.cart import Cart
from django.contrib import messages 


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
    cart = Cart(request)  # Получаем текущую корзину
    if len(cart) == 0:  # Проверяем, пуста ли корзина
        messages.error(request, "Корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('cart:cart_detail')  # Перенаправляем на страницу корзины

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)# Сохраняем форму без записи в базу данных
            order.total_price = cart.get_total_price() # Общая сумма заказа
            order.products = ", ".join([f"{item['product']} (x{item['quantity']})" for item in cart])  # Формируем список товаров с их количеством
            order.save()    # Сохраняем заказ в базу данных
            cart.clear()  # Очищаем корзину после оформления заказа
            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('success')  
    else:
        form = OrderForm()
    # Отображаем форму для оформления заказа
    return render(request, 'main/layout.html', {'form': form})

# Страница успешного заказа
def success(request):
    return render(request, 'main/success.html')