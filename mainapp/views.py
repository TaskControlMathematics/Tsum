from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse


def mainpage(request):
    return render(request, 'mainpage.html', locals())


def product_info(request, product_id):
    images = Product.objects.get(id=product_id).image_array
    imgs = images.split(',')
    prod_info = Product.objects.get(id=product_id)
    cat = prod_info.category
    cats = []
    ids = []
    cats.append(cat)
    ids.append(cat.id)
    parent = Categories.objects.get(id=cat.id_parent.id)
    while True:
        cat = Categories.objects.get(id=parent.id)
        cats.append(cat)
        ids.append(cat.id)
        if cat.id_parent is None:
            break
        parent = Categories.objects.get(id=cat.id_parent.id)
    cats.reverse()
    ids.reverse()
    cat_tree = zip(cats, ids)

    return render(request, 'product.html', locals())


def reg(request):
    signupform = SignUpForm()
    if request.POST:
        signupform = SignUpForm(request.POST)
        if signupform.is_valid():
            signupform.save()
            return HttpResponseRedirect('/')
    return render(request, 'reg.html', locals())


def auth(request):
    authform = AuthForm()
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'auth.html', locals())


def category(request, id_category):
    categories = Categories.objects.get(id=id_category)
    products = Product.objects.filter(category_tree__contains=categories.category)
    brands = []
    for item in products:
        brands.append(item.brand)
    brands = list(set(brands))
    if request.GET:
        request_brands = []
        for item in request.GET:
            if 'brand' in item:
                request_brands.append(item.split('_')[1])
        products = Product.objects.filter(category_tree__contains=categories.category, brand__in=request_brands)
        return render(request, 'category.html', locals())
    return render(request, 'category.html', locals())


def basket_adding(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    count = data.get("count")

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                 defaults={"count": count})

    if not created:
        if data.get('inform'):
            print('qwe')
            new_product.count = int(count)
            new_product.save(force_update=True)
        else:
            new_product.count += int(count)
            new_product.save(force_update=True)

    products_total_count = ProductInBasket.objects.filter(session_key=session_key).count()
    return_dict["products_total_count"] = products_total_count

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    if request.POST.get('isdelete'):
        print(request.POST)
        product_id = request.POST.get('id_product')
        product = ProductInBasket.objects.get(session_key=session_key,id=product_id)
        product.delete()
    return render(request, 'checkout.html', locals())


def cart(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    if request.POST:
        print(request.POST)
        delivery = request.POST['delivery_select']
        name = request.POST['name']
        sirname = request.POST['sirname']
        phone = request.POST['phone']
        email = request.POST['email']
        comment = request.POST['comment']
        user = request.user
        order = Order.objects.create(user=user, name=name, sirname=sirname, phone=phone, email=email, comment=comment,
                                     delivery=delivery)
        total_price = 0
        for product in products_in_basket:
            ProductInOrder.objects.create(order=order, product=product.product, count=product.count,
                                          total_price=product.total_price, price_per_item=product.price_per_item)
            total_price += product.total_price
        order.total_price = total_price
        order.save()

    return render(request, 'cart.html', locals())
