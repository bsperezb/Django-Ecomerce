from django.contrib import admin

from .models import Address, Coupon, Item, Order, OrderItem, Payment, Session


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = "Update orders to refound granted"


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "session",
        "user",
        "ordered",
        "being_delivered",
        "received",
        "refund_requested",
        "refund_granted",
        "billing_address",
        "shipping_address",
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

    list_display_links = [
        "session",
        "billing_address",
        "payment",
        "coupon",
        "shipping_address",
    ]

    search_fields = ["user__username", "reference", "session__session_number"]

    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "street_address",
        "apartment_address",
        "country",
        "zip",
        "address_type",
        "default",
    ]

    list_filter = ["address_type", "default", "country"]
    search_fields = ["user", "street_address", "apartment_address", "zip"]


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ("start_date",)


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon)
admin.site.register(Session, SessionAdmin)
