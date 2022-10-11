from django.contrib import admin
from .models import Users

class DatanetAdmin(admin.ModelAdmin):
    list_display = ('username','email','password','salt')

# Register your models here.
admin.site.register(Users, DatanetAdmin)