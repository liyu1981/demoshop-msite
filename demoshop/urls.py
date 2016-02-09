from django.conf.urls import url
from demoshop.views import ProductsView, DetailView, CartView
from demoshop.views import index, addToCart, pay
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^products$', ProductsView.as_view(), name='products'),
    url(r'^detail$', DetailView.as_view(), name='detail'),
    url(r'^cart$', CartView.as_view(), name='cart'),
    url(r'^addtocart$', addToCart, name='addtocart'),
    url(r'^pay$', pay, name='pay'),
    url(r'^thankyou$',
        TemplateView.as_view(template_name="demoshop/thankyou.html"),
        name='thankyou'),
    url(r'^$', index, name='index'),
]
