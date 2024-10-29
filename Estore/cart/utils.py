from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError

from products.models import ProductVariationOptionData


class CartSessionManager:
    KEY_NAME = "cart"
    ADD_ACT = 'add'
    REMOVE_ACT = 'remove'
    INCREASE_ACT = 'increase'
    DECREASE_ACT = 'decrease'
    ACTIONS = [ADD_ACT, REMOVE_ACT, INCREASE_ACT, DECREASE_ACT]

    def __init__(self, request, variation_option_id: int | str) -> None:
        self.request = request
        self._session = request.session
        self._action = request.GET.get('action')
        self._variation_option_id = variation_option_id
        self._option_obj = get_object_or_404(
            ProductVariationOptionData, pk=variation_option_id
        )
        self._product_obj = self._option_obj.product

        self._cart: dict = self.get_or_create_cart()

    def _validate_action(self):
        """raises ValidationError if the action is not available"""
        if self._action not in self.ACTIONS:
            raise ValidationError(
                "unavailable action",
                code="invalid_cart_action",
                params={"action": self._action},
            )

    def manage(self):
        self._validate_action()
        action_dict = {
            self.ADD_ACT: self.add_to_cart,
            self.INCREASE_ACT: self.increase_from_cart,
            self.REMOVE_ACT: self.remove_from_cart,
            self.DECREASE_ACT: self.decrease_from_cart,
        }

        action_dict[self._action]()

    def get_or_create_cart(self):
        """get or creates the cart like an empty dict if it does not exists."""
        if not self._session.get(self.KEY_NAME, False):
            self._session[self.KEY_NAME] = {}
            self._session.save()
        return self._session[self.KEY_NAME]

    def update_session_cart(self):
        """set the cart to the session and saves the session"""
        self._session[self.KEY_NAME] = self._cart
        self._session.save()

    def add_to_cart(self):
        """add the given variation option to the cart."""
        added = True
        if self._variation_option_id not in self._cart:
            self._cart[self._variation_option_id] = {"qtd": 1}
            self.update_session_cart()

        elif self._option_obj.stock > self._cart[self._variation_option_id]["qtd"]:
            self._cart[self._variation_option_id]["qtd"] += 1
            self.update_session_cart()

        elif self._option_obj.stock <= self._cart[self._variation_option_id]["qtd"]:
            messages.warning(
                self.request,
                f"{self._product_obj.name} has no stock available.",
            )
            added = False

        if added and self._action == self.ADD_ACT:
            messages.success(self.request, f"{self._product_obj.name} added to the cart.")

    def remove_from_cart(self):
        """remove an item of the cart"""
        if self._variation_option_id in self._cart:
            self._cart.pop(self._variation_option_id)
            self.update_session_cart()
            messages.warning(
                self.request,
                f"{self._product_obj.name} removed from the cart.",
            )
        else:
            messages.error(self.request, "product is not in the cart.")

    def increase_from_cart(self):
        """increase the quantity of the option in the cart"""
        self.add_to_cart()

    def decrease_from_cart(self):
        """decrease the qtd of the given variation option in the cart"""
        if self._cart[self._variation_option_id]['qtd'] > 1:
            self._cart[self._variation_option_id]['qtd'] -= 1
            self.update_session_cart()
        else:
            messages.warning(self.request, 'the minimum number of items are 1.')
