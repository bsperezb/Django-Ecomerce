from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (("S", "Stripe"), ("P", "PayPal"))


class CheckoutForm(forms.Form):
    """
    This is a Checkout Form
        * street_address
        * apartment_address
        * country
        * zip
        * same_billing_address
        * save_info
        * payment_option
    """

    street_address = forms.CharField(
        required=True,
        label="Address",
        widget=forms.TextInput(
            attrs={
                "placeholder": "1234 Main St",
                "class": "form-control",
                "id": "address",
            }
        ),
    )
    apartment_address = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apartment or suite",
                "class": "form-control",
                "id": "address-2",
            }
        ),
    )
    country = CountryField(blank_label="(select country)").formfield(
        required=False,
        widget=CountrySelectWidget(
            attrs={
                "class": "custom-select d-block w-100",
            }
        ),
    )
    zip = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "zip",
            }
        ),
    )

    same_shipping_address = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )
    save_info = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )

    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        required=True,
        widget=forms.RadioSelect,
    )


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Promo code",
                "aria-label": "Recipient's username",
                "aria-describedby": "basic-addon2",
            }
        )
    )
