from django.urls import path

from .views import (
    AddCouponView,
    CheckoutView,
    HomeView,
    ItemDetailView,
    Listen_payment_report,
    OrderSummaryView,
    PaymentView,
    RequestRefundView,
    add_to_cart,
    payment_redirect,
    remove_from_cart,
    remove_single_item_from_cart,
    setting_account_order,
)

app_name = "coreapp"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product/<slug>/", ItemDetailView.as_view(), name="product"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove_from_cart/<slug>/", remove_from_cart, name="remove_from_cart"),
    path(
        "remove-item-from-cart/<slug>/",
        remove_single_item_from_cart,
        name="remove-single-item-from-cart",
    ),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/redirect/", payment_redirect, name="payment-redirect"),
    path("add-coupon/", AddCouponView.as_view(), name="add-coupon"),
    path("request-refund/", RequestRefundView.as_view(), name="request-refund"),
    path("setting-account-order/", setting_account_order, name="setting-account-order"),
    path("Listen-payment-report/", Listen_payment_report, name="Listen-payment-report"),
    # path('payment/<payment_option>', PaymentView.as_view(), name='payment')
]
