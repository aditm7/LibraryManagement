from django.contrib import admin
from main.models import userinfo,book,booking

# Register your models here.
admin.site.register(book)
admin.site.register(booking)
admin.site.register(userinfo)