from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from config.settings.base import WOMPI_PUBLIC_KEY

from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Address, Coupon, Item, Order, OrderItem, Payment, Refund
from .payment import (
    get_amount_by_id,
    get_reference_by_id,
    get_status_by_id,
    random_reference,
)


# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"object": order}
            # import ipdb;ipdb.set_trace()

            return render(self.request, "order-summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def is_valid_form(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"form": form, "order": order, "DISPLAY_FORM": False}

            shipping_address_qs = Address.objects.filter(
                user=self.request.user, address_type="S", default=True
            )
            if shipping_address_qs.exists():
                context.update({"default_shipping_address": shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user, address_type="B", default=True
            )
            if billing_address_qs.exists():
                context.update({"default_billing_address": billing_address_qs[0]})

            return render(self.request, "checkout-page.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect("coreapp:home")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        # import ipdb; ipdb.set_trace()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                # Shipping address form
                use_default_shipping = form.cleaned_data.get("use_default_shipping")
                if use_default_shipping:
                    print("Use the defaul shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user, address_type="S", default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()

                    else:
                        messages.info(self.request, "No available")
                        return redirect("coreapp:checkout")
                else:
                    shipping_address1 = form.cleaned_data.get("shipping_address")
                    shipping_address2 = form.cleaned_data.get("shipping_address2")
                    shipping_country = form.cleaned_data.get("shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")
                    # payment_option = form.cleaned_data.get("payment_option")
                    if is_valid_form(
                        [shipping_address1, shipping_zip, shipping_country]
                    ):

                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type="S",
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            "set_default_shipping"
                        )
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(
                            self.request,
                            "please fill in the requirement shipping address fields",
                        )
                    # end Shipping address form

                # Billing address form
                use_default_billing = form.cleaned_data.get("use_default_billing")
                same_billing_address = form.cleaned_data.get("same_billing_address")

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    address_qs = Address.objects.filter(
                        user=self.request.user, address_type="B", default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()

                    else:
                        messages.info(
                            self.request, "No default billing addres available"
                        )
                        return redirect("coreapp:checkout")
                else:
                    print("user is entering a new billing address")
                    billing_address1 = form.cleaned_data.get("billing_address")
                    billing_address2 = form.cleaned_data.get("billing_address2")
                    billing_country = form.cleaned_data.get("billing_country")
                    billing_zip = form.cleaned_data.get("billing_zip")
                    if is_valid_form([billing_address1, billing_zip, billing_country]):

                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type="B",
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            "set_default_billing"
                        )
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(
                            self.request,
                            "please fill in the requirement billing address fields",
                        )
                    # End Billing addres form

                return redirect("coreapp:payment")
            messages.warning(self.request, "Failed checkout")
            return redirect("coreapp:checkout")

        except ObjectDoesNotExist:
            messages.warning(self.request, "you do not have an active order")
            return redirect("coreapp:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):

        try:
            form = CouponForm()
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.billing_address:
                amount = int(order.get_total() * 100)
                reference = random_reference()

                context = {
                    "order": order,
                    "WOMPI_PUBLIC_KEY": WOMPI_PUBLIC_KEY,
                    "reference": reference,
                    "amount": amount,
                    "form": form,
                    "DISPLAY_FORM": True,
                }
                order.reference = reference
                order.save()
                return render(self.request, "payment.html", context)
            else:
                messages.warning(self.request, "you have not added a  billing address ")
                return redirect("coreapp:checkout")
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect("core:home")


@login_required
def payment_redirect(request):
    id = request.GET.get("id")
    status = get_status_by_id(id)
    reference = get_reference_by_id(id)
    amount = get_amount_by_id(id)
    order = Order.objects.get(user=request.user, ordered=False, reference=reference)
    # billing_address verification
    try:
        billing_address = Address.objects.filter(user=request.user)[0]
    except ObjectDoesNotExist:
        messages.warning(request, "Your may add a billing addres")
        return redirect("coreapp:checkout")

    if status == "APPROVED":
        # create payment
        payment = Payment()
        payment.wompi_id = id
        payment.user = request.user
        payment.amount = amount / 100
        # payment.reference = reference
        payment.save()

        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.billing_address = billing_address
        order.ordered = True
        order.payment = payment
        order.reference = reference
        order.save()

        messages.success(
            request,
            f"Your order was Successful! \nthis is your payment reference: {reference}",
        )

        return redirect("coreapp:home")

    elif status == "DECLINED":
        messages.warning(request, "Your payment was Declined!")
        return redirect("coreapp:order-summary")
    elif status == "VOIDED":
        messages.warning(request, "Your order was Voided!")
        return redirect("coreapp:order-summary")
    else:
        messages.warning(
            request, "Something was wrong, if the problem persists please contact us"
        )
        return redirect("coreapp:order-summary")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificar el orden de los items en order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item cuantity was updated")
            return redirect("coreapp:order-summary")
        else:
            messages.info(request, "This item was added to your car")
            order.items.add(order_item)
            return redirect("coreapp:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your car")
        return redirect("coreapp:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificar si el item ordenado está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was remove from your cart")
            return redirect("coreapp:order-summary")
        else:
            # add a message saying the user doesn't have a item
            messages.info(request, "This item was not in your cart")
            return redirect("coreapp:product", slug=slug)

    else:
        messages.info(request, "yo don't have an active order")
        return redirect("coreapp:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # verificar si el item ordenado está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was update from your cart")
            return redirect("coreapp:order-summary")
        else:
            # add a message saying the user doesn't have a item
            messages.info(request, "This item was not in your cart")
            return redirect("coreapp:product", slug=slug)

    else:
        messages.info(request, "yo don't have an active order")
        return redirect("coreapp:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return False


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=self.request.user, ordered=False)
                if get_coupon(self.request, code):
                    order.coupon = get_coupon(self.request, code)
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                return redirect("coreapp:payment")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("coreapp:payment")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {"form": form}
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            reference = form.cleaned_data.get("reference")
            message = form.cleaned_data.get("message")
            email = form.cleaned_data.get("email")

            try:
                order = Order.objects.get(reference=reference)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, "Your request was received")
                return redirect("coreapp:request-refund")
            except ObjectDoesNotExist:
                messages.warning(self.request, "This order does not exist")
                return redirect("coreapp:request-refund")
