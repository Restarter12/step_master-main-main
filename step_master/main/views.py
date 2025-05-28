from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import OrderForm
from cart.cart import Cart
from django.contrib import messages 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile
from .models import ContactMessage
# Отображение списка товаров с фильтрацией по категориям
def product_list(request):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('categories') 
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
    product = get_object_or_404(Product, id=id, slug=slug, available=True) 
    cart_product_form = CartAddProductForm() 
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

# регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя и профиль через форму
            login(request, user)  # Логиним пользователя
            return redirect('home')  # Редирект на главную страницу
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')


# проверка на регисрацию
@login_required(login_url='login')  # Если не авторизован, редиректит на страницу логина
def submit_order(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, "Корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.products = ", ".join([f"{item['product']} (x{item['quantity']})" for item in cart])
            order.save()
            cart.clear()
            return redirect('success')
    else:
        form = OrderForm()

    
    return render(request, 'main/tovar.html', {'form': form})

# история заказа в профиле
@login_required
def profile(request):
    # Получаем все заказы пользователя
    orders = Order.objects.filter(user=request.user)

    return render(request, 'main/profile.html', {
        'user': request.user,
        'orders': orders
    })

# удаление заказа
@login_required
def delete_order(request, order_id):
    # Получаем заказ по ID
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Удаляем заказ
    order.delete()

    # Отправляем сообщение об успехе
    messages.success(request, "Ваш заказ был удалён.")

    # Перенаправляем обратно на страницу профиля или на другую страницу
    return redirect('profile')  


# создание профиля
@login_required
def profile(request):
    # Создаем профиль пользователя, если его нет
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Получаем заказы пользователя
    orders = Order.objects.filter(user=request.user)

    return render(request, 'main/profile.html', {
        'user': request.user,
        'profile': profile,
        'orders': orders
    })


# форма обратной связи
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Ваше сообщение отправлено! Мы ответим вам в ближайшее время.")
            return redirect("about")  
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")

    return render(request, "main/about.html")