from django.forms import inlineformset_factory

from .models import Basket, BasketItem

BasketFormSet = inlineformset_factory(
    Basket,
    BasketItem,
    fields=('quantity', ),
    extra=0,
    can_delete=True
)
