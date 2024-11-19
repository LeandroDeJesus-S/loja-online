from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from addresses.models import UserAddress
from .forms import UserForm, UserAddressForm, AddressForm
from django.contrib import messages


class Profile(LoginRequiredMixin, View):
    template_name = "static/html/user_profile/show_profile.html"
    readonly_forms = True

    def get(self, *args, **kwargs):
        user_addr_instance = None
        address_instance = None
        user_addr_instance = UserAddress.objects.filter(
            user=self.request.user
        ).first()

        context = {
            "user_form": UserForm(
                instance=self.request.user, readonly=self.readonly_forms
            ),
            "user_address_form": UserAddressForm(
                instance=user_addr_instance,
                readonly=self.readonly_forms,
                initial={'user': self.request.user}
            ),
            "address_form": AddressForm(
                instance=address_instance, readonly=self.readonly_forms
            ),
        }
        return render(self.request, self.template_name, context)


class EditProfile(Profile):
    readonly_forms = False
    template_name = "static/html/user_profile/edit_profile.html"

    def post(self, *args, **kwargs):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        address_form = AddressForm(self.request.POST)
        user_address_form = UserAddressForm(self.request.POST)

        context = {
            "user_form": user_form,
            "user_address_form": user_address_form,
            "address_form": address_form,
        }

        if not user_form.is_valid() or not address_form.is_valid():
            return render(self.request, self.template_name, context)

        user = user_form.save()
        address = address_form.save()

        if not user_address_form.is_valid():
            return render(self.request, self.template_name, context)

        user_address = user_address_form.save(commit=False)
        user_address.user = user
        user_address.address = address
        address.save()
        user_address.save()
        return redirect("user_profile")


class DisableProfile(LoginRequiredMixin, View):
    template_name = 'static/html/user_profile/disable_profile.html'
    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)
    
    def post(self, *args, **kwargs):
        referer_url = self.request.META.get('HTTP_REFERER')
        expected_referer = f'http://{self.request.get_host()}{reverse("disable_profile")}'
        if referer_url != expected_referer:
            return redirect('user_profile')
        
        self.request.user.is_active = False
        self.request.user.save()
        messages.info(self.request, 'Account disabled successfully.')
        return redirect('home')
