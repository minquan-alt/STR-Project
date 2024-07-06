from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category, Remarkable, Purchase
from .forms import ProductForm, RemarkableForm, PurchaseForm
from collections import defaultdict
from decimal import Decimal
from django.db.models import Sum

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
    context ={'page':page}
    return render(request, 'coffee/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'coffee/login_register.html', {'form':form})

def home(request):
     #request.GET.get('q'):lấy giá trị của tham số 'q' từ query string của URL
    #kiểm tra liệu tham số q có tồn tại không.
    #nếu không tồn tại đặt giá trị 'q' là chuỗi rỗng 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #lấy thêm tham số p để lọc danh sách loại thức ăn đồ uống
    category_filter = request.GET.get('p')
    
    if category_filter:
    # vừa lọc danh mục sản phẩm thuộc loại này vừa liệt kê các sản phẩm đó ra
        products = Product.objects.filter(name__icontains=q, category__name__iexact=category_filter)
    else:
        products = Product.objects.filter(name__icontains=q)
    categories = Category.objects.all()
    product_count = products.count()
    product_remarkables = Remarkable.objects.all()
    context = {'products': products, 'categories': categories, 'product_count': product_count, 'product_remarkables': product_remarkables}
    return render(request, 'coffee/home.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    product_remarkables = product.remarkable_set.all()

    if request.method == 'POST':
        remarkable = Remarkable.objects.create(
            user = request.user,
            product = product,
            body = request.POST.get('body')
        )
        return redirect('product', pk=product.id)
    
    context = {'product':product, 'product_remarkables': product_remarkables}
    return render(request, 'coffee/product.html', context)

@login_required(login_url='login')
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'coffee/product_form.html', context)

@login_required(login_url='login')
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.user != product.host:
        return HttpResponse('Your are not allowed here')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'coffee/product_form.html', context)

@login_required(login_url='login')
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    if request.user != product.host:
        return HttpResponse('Your are not allowed here')

    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'coffee/delete_product.html',{'obj':product})

@login_required(login_url='login')
def updateRemarkable(request, pk):
    remarkable = Remarkable.objects.get(id=pk)
    form = RemarkableForm(instance=remarkable)

    if request.user != remarkable.user:
        return HttpResponse('Your are not allowed here')

    if request.method == 'POST':
        form = RemarkableForm(request.POST, instance=remarkable)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'coffee/product_form1.html', context)

@login_required(login_url='login')
def deleteRemarkable(request, pk):
    remarkable = Remarkable.objects.get(id=pk)

    if request.user != remarkable.user:
        return HttpResponse('Your are not allowed here')
    
    if request.method == 'POST':
        remarkable.delete()
        return redirect('home')
    return render(request, 'coffee/delete_product.html',{'obj':remarkable})

@login_required(login_url='login')
def purchaseProduct(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = PurchaseForm()

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.product = product
            purchase.save()
            return redirect('pay-a-bill')

    context = {'form': form, 'product': product}
    return render(request, 'coffee/purchase_form.html', context)

@login_required(login_url='login')
def pay_a_bill(request):
    purchases = Purchase.objects.filter(user=request.user)
    
    # Dictionary to store product, total quantity, and total price
    product_totals = defaultdict(lambda: {'total_quantity': 0, 'total_price': Decimal('0.0')})
    
    for purchase in purchases:
        product_totals[purchase.product]['total_quantity'] += purchase.quantity
        product_totals[purchase.product]['total_price'] += Decimal(purchase.quantity) * purchase.product.price
    
    # Calculate grand total
    grand_total = sum(totals['total_price'] for totals in product_totals.values())
    
    context = {
        'product_totals': dict(product_totals),
        'grand_total': grand_total,
    }
    return render(request, 'coffee/pay_a_bill.html', context)



