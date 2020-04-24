from django.urls import reverse
from django.shortcuts import redirect


class BasketNotEmptyMixin:
    """Prevent user from accessing view if basket is empty"""

    def dispatch(self, request, *args, **kwargs):
        # check basket is part of request object
        if hasattr(self.request, 'basket'):
            basket = self.request.basket
        else:
            basket = None
        # make sure the user's basket is not empty
        if not basket or basket.count() == 0:
            return redirect(reverse('basket'))

        return super().dispatch(request, *args, **kwargs)
