import django
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import (render,
                              get_object_or_404,
                              redirect,
                              )
from django.utils import timezone
from django.views.generic.base import View
from .models import Item, OrderItem, Order, BillingAddress
from django.views.generic import ListView, DetailView
from .forms import CheckoutForm

# Create your views here.


# def home(request):
#   context = {
#       "items": Item.objects.all()
#   }
#   return render(request, "home.html", context)

class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10

class OrderSummaryView(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render( self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("/")
            


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm
        context = {
            'form': form
        }
        return render(self.request, "checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # Then add functionality for this fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    zip = zip,
                    country = country,
                )
                billing_address.save()
                order.biilling_address = billing_address
                order.save()
                # TODO: Add redirect to de selected payment option (stripe and other)
                return redirect( 'coreapp:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('coreapp:checkout')


        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("coreapp:order-summary")




@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False

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
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # verificar si el item ordenado está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was remove from your cart")
            return redirect("coreapp:order-summary")
        else:
            #add a message saying the user doesn't have a item
            messages.info(request, "This item was not in your cart")
            return redirect("coreapp:product", slug=slug)

    else:
        messages.info(request, "yo don't have an active order")
        return redirect("coreapp:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        # verificar si el item ordenado está en la orden
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was update from your cart")
            return redirect("coreapp:order-summary" )
        else:
            #add a message saying the user doesn't have a item
            messages.info(request, "This item was not in your cart")
            return redirect("coreapp:product", slug=slug)

    else:
        messages.info(request, "yo don't have an active order")
        return redirect("coreapp:product", slug=slug)