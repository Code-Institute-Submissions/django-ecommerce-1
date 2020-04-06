from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages

from .models import Basket, BasketItem
from products.models import Product

# Create your views here.


def view_basket(request):

    if request.basket:
        message = 'basket exists'
    else:
        message = 'no basket'

    context = {'message': message}

    return render(request, 'basket/basket.html', context)


# @transaction.atomic
def add_to_basket(request, product):
    product = get_object_or_404(Product, id=product)
    basket = request.basket

    if not basket:
        # create new basket and store in session var for accessing
        basket = Basket.objects.create(user=request.user)
        request.session['basket_id'] = basket.id

    # basket exists, add or update basket item
    basket_item, new = BasketItem.objects.get_or_create(
        basket=basket, product=product)
    print(request.basket)

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


def remove_from_basket(request, product):
    return HttpResponse('<h1>Remove from Basket</h1>')


def update_basket(request):
    return HttpResponse('<h1>Update Basket</h1>')
