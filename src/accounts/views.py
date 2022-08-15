from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView

# from django_learn_helper import settings
from .apps import user_registered
from .forms import AccountRegistrationForm, CustomAuthenticationForm, ActivationEmailConfirmationForm
from .forms import AccountUpdateForm
from .forms import AccountRegistrationForm, ActivationEmailConfirmationForm
from .utils import signer


class AccountRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:login')
    form_class = AccountRegistrationForm


class AccountRegistrationDoneView(TemplateView):
    template_name = 'accounts/registration_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/activation_done.html'
        user.is_active = True
        user.is_activated = True
        print("User created")
    user.save()

    return render(request, template)


# def activation_email_confirmation(request):
#     if request.method == "GET":
#         form = ActivationEmailConfirmationForm(request)
#         context = {"form": form}
#         template_name = "accounts/activation_email_confirmation.html"
#         return render(request, template_name, context)
#     elif request.method == "POST":
#         form = ActivationEmailConfirmationForm(request)
#         if form.is_valid() or not form.is_valid():
#             user = request.user
#             user.email = request.POST["email"]
#             user.save()
#             user_registered.send(AccountRegistrationForm, instance=request.user)
#             print(request.POST)
#             return redirect(reverse_lazy("words:home"))

def activation_email_confirmation(request):
    user_registered.send(AccountRegistrationForm, instance=request.user)
    return redirect(reverse_lazy("accounts:profile"))


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'

    # form_class = CustomAuthenticationForm

    def get_redirect_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('index')

    # def confirm_login_allowed(self, user):
    #     print("\nwpirjgi0erghoetohrtouhogurtegourtou\n")
    #     if not user.is_activated:
    #         print('\nAEFJPEWFJPIWREJIPRJIERJIORE\n')
    #         # raise ValidationError(
    #         #     self.error_messages["inactive"],
    #         #     code="inactive",
    #         # )
    #     super().confirm_login_allowed(user)
    #


class AccountLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


@login_required
def account_profile_view(request):
    return render(request, 'accounts/profile.html')


class AccountUpdateProfileView(UpdateView, LoginRequiredMixin):
    template_name = 'accounts/profile_update.html'
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')
    form_class = AccountUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
