from django import template

from shop.coreapp.models import Order, Session
from shop.coreapp.session import random_session_id

register = template.Library()


@register.filter
def cart_item_count(request):
    if request.user.is_authenticated:
        # verificar si existen obetos en carrito
        qs = Order.objects.filter(user=request.user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
        else:
            return 0
    else:

        session_number = request.session.get("session_number", random_session_id())
        session, created = Session.objects.get_or_create(session_number=session_number)
        qs = Order.objects.filter(session=session, ordered=False)
        if qs.exists():
            return qs[0].items.count()
        return 0
