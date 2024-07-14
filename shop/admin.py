from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'weigh', 'height', 'deep', 'color', 'get_photo')
    list_editable = ('price', 'quantity', 'weigh', 'height', 'deep', 'color')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price', 'category')
    inlines = [GalleryInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Картинка'


# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Gallery)
admin.site.register(Review)
admin.site.register(FavouriteProducts)
# admin registration for Order
admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)

