from django.contrib import admin
from . import models

class SubCategoryInline(admin.TabularInline):
    model = models.SubCategory
    
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline
    ]
    
admin.site.register(models.Category, CategoryAdmin)
