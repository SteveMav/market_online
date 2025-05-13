from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'session_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name', 'session_id')
    readonly_fields = ('created_at', 'updated_at')
