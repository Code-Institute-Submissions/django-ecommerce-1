from django import forms

from .models import Order

from crispy_forms.bootstrap import Field, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Fieldset, Layout


class OrderDetailsForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'status', 'last_updated', 'order_date', 'stripe_id')

    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        # create form structure using crispy forms
        self.helper = FormHelper()
        self.helper.form_id = 'shipping-details-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Billing Details',
                     Div(
                         Field('billing_name',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         Field('billing_address',
                               wrapper_class='col-12 col-md-8',
                               readonly='readonly'),

                         Field('billing_post_code',
                               wrapper_class='col-12 col-md-4',
                               readonly='readonly'),

                         Field('billing_city',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         Field('billing_country',
                               wrapper_class='col-12 col-md-6',
                               readonly='readonly'),

                         css_class='row')
                     ),
            Fieldset('Shipping Details',
                     Div(
                         Field('shipping_name',
                               wrapper_class='col-12 col-md-6'),

                         Field('shipping_address',
                               wrapper_class='col-12 col-md-8'),

                         Field('shipping_post_code',
                               wrapper_class='col-12 col-md-4'),

                         Field('shipping_city',
                               wrapper_class='col-12 col-md-6'),

                         Field('shipping_country',
                               wrapper_class='col-12 col-md-6'),

                         css_class='row')
                     )
        )


class PaymentProcessingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # stripe payment client secret token
        stripe_secret = kwargs.pop('stripe_secret', None)
        payment_amount = kwargs.pop('payment_amount', None)

        super(PaymentProcessingForm, self).__init__(*args, **kwargs)
        # create form structure using crispy forms

        if not stripe_secret:
            stripe_secret = ''

        if not payment_amount:
            payment_amount = ''

        self.helper = FormHelper()
        self.helper.form_id = 'payment-form'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('checkout_complete')
        self.helper.layout = Layout(
            Div(
                Div(css_id='card-element'),
                Div(css_id='card-errors', role='alert'),
                css_class='form-row'
            ),
            StrictButton(
                f'Pay €{payment_amount}',
                css_class='btn btn-info btn-sm',
                css_id='payment-button',
                data_secret=stripe_secret,
                type='submit'
            )
        )
