from copy import deepcopy
from allauth.account.views import LogoutView


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Copia os dados da sessão antes do logout
        session_data = deepcopy(request.session.get('cart', {}))

        # Realiza o logout chamando a view original
        response = super().dispatch(request, *args, **kwargs)

        # Restaura a sessão ou faz outra ação, se necessário
        request.session['cart'] = session_data
        request.session.save()

        return response
