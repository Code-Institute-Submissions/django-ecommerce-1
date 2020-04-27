import stripe

from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import OrderDetailsForm, PaymentProcessingForm


@login_required
def process_order(request):
    """Convert a user's basket (and basket items) into an order (with order
    items). This requires that payment is succesfully processed and stripe_id
    passed through"""

    if hasattr(request, 'basket'):
        basket = request.basket
    else:
        basket = None

    # user must have items in their basket before proceeding
    if not basket or basket.count() == 0:
        return redirect(reverse('basket'))

    # set api key to enable use across POST and GET
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    if request.method == 'POST':
        shipping_form = OrderDetailsForm(request.POST)
        payment_form = PaymentProcessingForm(request.POST)

        if shipping_form.is_valid():

            # check that stripe token exists
            stripe_id = request.POST['stripe-token']
            if stripe_id:
                try:
                    # make sure the token is valid - if not stripe will raise
                    # InvalidRequestError, captured below
                    stripe.PaymentIntent.retrieve(stripe_id)

                    # payment validated, convert user's basket into order
                    order = basket.create_order(
                        order_details=shipping_form.cleaned_data,
                        stripe_id=stripe_id)

                    if order:
                        # empty session variable and basket object
                        request.session['basket_id'] = None
                        request.basket = None

                        messages.success(request,
                                         'Your payment has been received. You'
                                         ' will receive an email when your '
                                         'order has been shipped.')
                        return redirect(reverse('home'))
                except stripe.error.CardError:
                    messages.error(
                        'Your payment card has been declined. Please try '
                        'another card.')
                except Exception as e:
                    print(e)
                    messages.error(request,
                                   'There was a problem processing your order,'
                                   ' please try again.')

                return redirect(reverse('checkout'))
        else:

            return render(request, 'checkout/order_processing.html', {
                'shipping_form': shipping_form,
                'payment_form': payment_form
            })
    else:
        # setup shipping details form
        initial = {}
        user = request.user
        # pre-populate details with user information
        # form field prefixes
        prefix = ('billing_', 'shipping_')
        for _prefix in prefix:
            initial[_prefix + 'name'] = user.first_name + ' ' + user.last_name
            initial[_prefix + 'address'] = user.address
            initial[_prefix + 'post_code'] = user.post_code
            initial[_prefix + 'city'] = user.city
            initial[_prefix + 'country'] = user.country

        shipping_form = OrderDetailsForm(initial=initial)

        # setup payment form
        # convert order amount to stripe compatiable integer
        total = basket.total()
        total_stripe = int(total * 100)
        # setup stripe variables
        intent = stripe.PaymentIntent.create(
            amount=total_stripe,
            currency='eur',
            metadata={'integration_check': 'accept_a_payment'},
        )
        # pass-through client_secret to form as kwarg
        payment_form = PaymentProcessingForm(
            stripe_secret=intent.client_secret,
            payment_amount=total)

        return render(request, 'checkout/order_processing.html', {
            'shipping_form': shipping_form,
            'payment_form': payment_form
        })
