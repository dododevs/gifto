from django.contrib import admin

from gifto.models import GiftoUser, Category, Hobby, Product

admin.site.register(GiftoUser)
admin.site.register(Category)
admin.site.register(Hobby)
admin.site.register(Product)