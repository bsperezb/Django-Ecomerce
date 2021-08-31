import random
import string

import requests
from django.core.exceptions import ObjectDoesNotExist

from config.settings.base import WOMPI_PRIVATE_KEY, WOMPI_SANBOX_URL


def get_status_reference(reference):
    """
    The answer could be:
    *DECLINED
    *APPROVED
    *VOIDED
    *ERROR
    The url and toke corresponds to sandbox
    """
    token = "Bearer " + WOMPI_PRIVATE_KEY
    # token = 'Bearer prv_test_R6kUrYFWeeQYxPHSs7LkBXgKnvAoffVe'
    url = WOMPI_SANBOX_URL
    # url = 'https://sandbox.wompi.co/v1/transactions'
    headers = {"Authorization": token}
    params = {"reference": reference}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=3)
        resp_json = resp.json()
        return resp_json["data"][0]["status"]
    except ObjectDoesNotExist:
        return "Something went wrong, try again."


def get_status_by_id(id):
    url = "http://sandbox.wompi.co/v1/transactions/"
    url += id
    try:
        resp = requests.get(url, timeout=3)
        resp_json = resp.json()
        return resp_json["data"]["status"]
    except ObjectDoesNotExist:
        return "Something went wrong, try again."


def get_reference_by_id(id):

    url = "http://sandbox.wompi.co/v1/transactions/"
    url += id
    try:
        resp = requests.get(url, timeout=3)
        resp_json = resp.json()
        return resp_json["data"]["reference"]
    except ObjectDoesNotExist:
        return "Something went wrong, try again."


def get_amount_by_id(id):

    url = "http://sandbox.wompi.co/v1/transactions/"
    url += id
    try:
        resp = requests.get(url, timeout=3)
        resp_json = resp.json()
        return resp_json["data"]["amount_in_cents"]
    except ObjectDoesNotExist:
        return "Something went wrong, try again."


def random_reference():
    reference = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    # TODO compara referencia en base de datos y si es la misma, cambiar.
    return reference
