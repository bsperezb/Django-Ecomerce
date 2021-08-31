from django.contrib import admin

from .models import BillingAddress, Coupon, Item, Order, OrderItem, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "ordered"]


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
