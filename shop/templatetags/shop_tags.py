from django import template
from shop.models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_favorite_products(user):
    fav = FavouriteProducts.objects.filter(user=user)
    product = [i.product for i in fav]
    return product