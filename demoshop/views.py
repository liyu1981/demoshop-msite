import logging
import re
import time
import json
import uuid
from django.views.generic import TemplateView
from django.shortcuts import redirect
from models import Shop

logger = logging.getLogger(__name__)

def filterProducts(products, category):
    if category == 'ALL':
        return products
    r = []
    for product in products:
        if product['title'].endswith(category):
            r.append(product)
    return r

def findProduct(products, id):
    for product in products:
        if product['id'] == id:
            return product
    return None

def getPriceFromString(pricestring):
    r = re.search('^[\d.]+', pricestring)
    if r.group(0):
        return float(r.group(0))
    return 0

def calcTotal(cart):
    total = 0
    for product in cart:
        total = total + getPriceFromString(product['price'])
    return total

def calcTransRef(cart):
    c = []
    for product in cart:
      c.append({
        "title": product['title'],
        "price": product['price'],
        "image_link": product["image_link"]
      })
    trans = { "cart": c, "time": int(time.time()), "total": calcTotal(cart) }
    return json.dumps(trans)


class ProductsView(TemplateView):
    template_name = 'demoshop/products.html'

    def get_context_data(self, **kwargs):
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            if category and category and (category in Shop.getCategories()):
                Shop._current_category = category

        context = super(ProductsView, self).get_context_data(**kwargs)
        context['products'] = \
            filterProducts(Shop.getProducts(), Shop._current_category)
        context['categories'] = Shop.getCategories()
        context['currentCategory'] = Shop._current_category
        return context


class DetailView(TemplateView):
    template_name = 'demoshop/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        product = findProduct(Shop.getProducts(), self.request.GET['id'])
        if product:
            context['product'] = product
        return context;


class CartView(TemplateView):
    template_name = 'demoshop/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['products'] = Shop._cart
        context['total'] = calcTotal(Shop._cart)
        context['transref'] = calcTransRef(Shop._cart)
        context['userref'] = str(uuid.uuid4())
        return context;

def index(request):
    return redirect('demoshop:products')

def addToCart(request):
    product = findProduct(Shop.getProducts(), request.GET['id'])
    if product:
        Shop._cart.append(product)
    return redirect('demoshop:cart')

def pay(request):
    Shop._cart = []
    return redirect('demoshop:thankyou')
