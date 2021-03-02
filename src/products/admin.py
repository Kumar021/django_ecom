from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Product,Variation, Size, Color 

class ProductAdmin(admin.ModelAdmin):
	list_display  = ('title', 'slug', 'description', 'price', 'image_tag')

	#readonly_fields = ("image_tag", )

	def image_tag(self, obj):
		return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

	image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin) 


class ProductVariationAdmin(admin.ModelAdmin):
	list_display  = ('color', 'size', 'image_tag', 'price')

	def image_tag(self, obj):
		return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

	image_tag.short_description = 'Image'

admin.site.register(Variation, ProductVariationAdmin)


class ProductVariationSizeAdmin(admin.ModelAdmin):
	list_display  = ('name',)

admin.site.register(Size, ProductVariationSizeAdmin)


class ProductVariationColorAdmin(admin.ModelAdmin):
	list_display  = ('name',)

admin.site.register(Color, ProductVariationColorAdmin)