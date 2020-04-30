from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from .models import Basket, BasketItem
from products.models import Product
from .forms import BasketFormSet


def view_basket(request):
    if request.method == 'POST':
        formset = BasketFormSet(request.POST, instance=request.basket)

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Your basket has been updated.')

            formset = BasketFormSet(instance=request.basket)
        else:
            messages.error(
                request, 'Your basket could not be updated, please review any '
                'error messages below.')

    else:
        if hasattr(request, 'basket'):
            formset = BasketFormSet(instance=request.basket)
        else:
            formset = None

    context = {'formset': formset}

    return render(request, 'basket/basket.html', context)


@transaction.atomic
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if hasattr(request, 'basket') and request.basket is not None:
        # basket already exists
        basket = request.basket
    else:
        # no basket in request object - this is a new basket
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        # create new basket and store in session var for accessing
        basket = Basket.objects.create(user=user)
        request.session['basket_id'] = basket.id

    # basket exists (otherwise raise 404), add or update basket item
    basket_item, new = BasketItem.objects.get_or_create(
        basket=basket, product=product)

    if new:
        # new product in basket
        messages.success(request, f'{product.title} added to basket.')
    else:
        # product already exists
        # make sure that basket quantity does not exceed maximum amount
        if basket_item.quantity < 5:
            # update quantity
            basket_item.quantity += 1
            basket_item.save()
            messages.info(
                request, f'{product.title} quantity now \
                    {basket_item.quantity}.')
        else:
            messages.warning(
                request, 'You have the maximum permitted amount of this item \
                    in your basket, no more can be added.')

    return redirect(reverse('basket'))


@receiver(user_logged_in)
def get_basket(sender, user, request, **kwargs):
    """When user logs in, retrieve basket and merge with existing"""

    try:
        # does the user have a basket already stored in db
        existing_basket = Basket.objects.get(
            user=user, status=Basket.IN_PROGRESS)

        # check to see if added any items to basket before logging in
        if hasattr(request, 'basket'):
            new_items_basket = request.basket
            new_items = []

            try:
                # loop through new items and store as list of dictionaries
                for item in new_items_basket.basketitem_set.all():
                    new_items += [{
                        'product': item.product,
                        'quantity': item.quantity
                    }]

                # check list against existing basket, add new, update existing
                for item in new_items:
                    basket_item, new = BasketItem.objects.get_or_create(
                        basket=existing_basket, product=item['product'])

                    if new:
                        quantity = item['quantity']
                    else:
                        # add existing quantity to new basket quantity
                        quantity = basket_item.quantity + item['quantity']

                    # check quantity does not exceed maximum permissable amount
                    if quantity > 5:
                        quantity = 5
                        messages.warning(
                            request, f"Product '{item['product']}' exceeded the \
                                maximum quantity, quantity set to maximum \
                                    permittable amount.")
                    # set quantity and save object
                    basket_item.quantity = quantity
                    basket_item.save()
            except Exception as e:
                # capture exceptions coming from no basket items
                print(e)
                pass

            # provide feedback to user
            messages.info(
                request, "Your new items have been merged with your existing \
                    basket.")
            # remove anonymous basket, given contents merged into user basket
            new_items_basket.delete()

        # update session variable to enable middleware to set request.basket
        request.session['basket_id'] = existing_basket.id

    except Basket.DoesNotExist:
        # user account does not already have an 'in progress' basket
        # check to see if user created a basket anonymously
        # if so, attach it to the user's account
        basket_id = request.session.get('basket_id', False)

        if basket_id:
            try:
                basket = Basket.objects.get(
                    id=request.session['basket_id'], user=None)

                if basket:
                    # basket exists, update user to current user
                    basket.user = user
                    basket.save()
            except Basket.DoesNotExist:
                # user does not have a basket
                pass
