from django import forms
from django.contrib.auth import get_user_model
from addresses.models import UserAddress, Address


class BaseProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.readonly = kwargs.pop('readonly', False)
        super().__init__(*args, **kwargs)
        if self.readonly:
            for field in self.fields.values():
                field.disabled = True


class UserAddressForm(BaseProfileForm):
    class Meta:
        model = UserAddress
        fields = ['user', 'number', 'complement', 'address']
        widgets = {
            'user': forms.HiddenInput(),
            'address': forms.HiddenInput(),
        }


class AddressForm(BaseProfileForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'country', 'postal_code']


class UserForm(BaseProfileForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username']