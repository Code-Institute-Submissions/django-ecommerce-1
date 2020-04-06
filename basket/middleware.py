# from django.core.exceptions import ObjectDoesNotExist

from .models import Basket


class BasketMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check that a basket session exists
        basket_id = request.session.get('basket_id', False)
        if basket_id:
            try:
                # make sure the basket exists in the db
                basket = Basket.objects.get(id=basket_id)
                request.basket = basket
            except Basket.DoesNotExist:
                # basket not in db, unset variables
                request.session['basket_id'] = None
                request.basket = None

        response = self.get_response(request)

        return response
