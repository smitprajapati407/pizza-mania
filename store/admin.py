from django.contrib import admin
from store.models import Category,Pizaa

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']


@admin.register(Pizaa)
class PizaaAdmin(admin.ModelAdmin):
    list_display=['name','category','image','description','id','price'] 
    list_filter=['category']
    search_fields=['name']   

# Register your models here.
