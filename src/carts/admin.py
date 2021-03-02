from django.contrib import admin

from .models import Cart,Coupon

class CartAdmin(admin.ModelAdmin):
	list_display  = (
				'user',  
				'get_products',
				'get_colors',
				'quantity',
				'coupon', 
				'total', 
				'subtotal', 
				'updated',
				'timestamp',
			)

	def get_products(self, obj):
		return "\n".join([str(p.id) for p in obj.products.all()])

	def get_colors(self, obj):
		return "\n".join([str(c.id) for c in obj.colors.all()])

	

admin.site.register(Cart, CartAdmin)

admin.site.register(Coupon)