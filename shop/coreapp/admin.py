from django.contrib import admin

from .models import BillingAddress, Coupon, Item, Order, OrderItem, Payment


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = "Update orders to refound granted"


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
        "billing_address",
        "payment",
        "coupon",
    ]

    list_filter = [
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
    ]

    list_display_links = ["user", "billing_address", "payment", "coupon"]

    search_fields = ["user__username", "reference"]

    actions = [make_refund_accepted]


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
