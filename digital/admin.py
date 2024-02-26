from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm
# Register your models here.

from .forms import Category

admin.site.register(Gallery)
admin.site.register(ProductDescription)
admin.site.register(FavoriteProduct)
admin.site.register(Profile)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAdress)
admin.site.register(City)


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


class ParameterInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductDescription
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'get_image_category')
    prepopulated_fields = {'slug': ['title']}
    form = CategoryForm
    list_display_links = ('pk', 'title', 'get_image_category')

    def get_image_category(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="40">')
            except Exception as e:
                print(e)
                return '-'
        else:
            return '-'

    get_image_category.short_description = 'Картинка'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category')
    list_display_links = ('pk', 'title')
    list_filter = ['category', 'title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'price', 'quantity', 'edited_at', 'created_at', 'get_image_product')
    list_display_links = ('pk', 'title')
    inlines = [GalleryInline, ParameterInline]
    prepopulated_fields = {'slug': ['title']}
    list_editable = ('price', 'quantity')

    def get_image_product(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="100">')
            except Exception as e:
                print(e)
                return '-'
        else:
            return '-'

    get_image_product.short_description = 'Картинка товара'
