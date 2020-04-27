# from django.core.exceptions import ObjectDoesNotExist

from .models import Basket


class BasketMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check that a basket session exists
        basket_id = request.session.get('basket_id', False)

        try:
            if basket_id:
                # if session variable exists, store basket object in request
                # object to access from any view
                request.basket = Basket.objects.get(
                    id=basket_id,
                    status=Basket.IN_PROGRESS)
            else:
                # make sure user is logged in
                if request.user.is_authenticated:
                    # no session variable, check if user has basket in db
                    # store in request object
                    request.basket = Basket.objects.get(
                        user=request.user,
                        status=Basket.IN_PROGRESS)
        except Basket.DoesNotExist:
            # basket not in db, unset variables
            request.session['basket_id'] = None
            request.basket = None

        response = self.get_response(request)

        return response
