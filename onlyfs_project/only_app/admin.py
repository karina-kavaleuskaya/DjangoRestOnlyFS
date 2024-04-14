from django.contrib import admin
from only_app.models import Category, Discount, Product, ProductImage, Stock


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'category__name')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Stock)

