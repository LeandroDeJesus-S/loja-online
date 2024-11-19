from copy import deepcopy
from allauth.account.views import LogoutView


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        """copy the cart the user's logged out session"""
        session_data = deepcopy(request.session.get('cart', {}))
        response = super().dispatch(request, *args, **kwargs)
        request.session['cart'] = session_data
        request.session.save()
        return response
