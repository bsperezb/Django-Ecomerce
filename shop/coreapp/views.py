from django.contrib import messages
from django.shortcuts import (render,
                              get_object_or_404,
                              redirect,
                              )
from django.utils import timezone
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView


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


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def checkout(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, "checkout-page.html", context)


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
            return redirect("coreapp:product", slug=slug)
        else:
            messages.info(request, "This item was added to your car")
            order.items.add(order_item)
            return redirect("coreapp:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your car")
        return redirect("coreapp:product", slug=slug)


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
            return redirect("coreapp:product", slug=slug)
        else:
            #add a message saying the user doesn't have a item
            messages.info(request, "This item was not in your cart")
            return redirect("coreapp:product", slug=slug)

    else:
        messages.info(request, "yo don't have an active order")
        return redirect("coreapp:product", slug=slug)