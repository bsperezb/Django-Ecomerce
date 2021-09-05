import random
import string

from .models import Session

# from django.core.exceptions import ObjectDoesNotExist


def random_session_id():
    session = "".join(random.choices(string.ascii_uppercase + string.digits, k=30))
    return session


def random_session(request):
    session_number = request.session.get("session_number", random_session_id())
    session, created = Session.objects.get_or_create(session_number=session_number)
    request.session["session_number"] = session.session_number
    return session
