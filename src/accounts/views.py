from django.contrib import messages
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
from .apps import user_registered
from .forms import AccountUpdateForm
from .forms import AccountRegistrationForm
from .utils import signer


class AccountRegistrationView(CreateView):
    model = get_user_model()
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('accounts:login')
    form_class = AccountRegistrationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.GET.get('username', default='')
        initial['email'] = self.request.GET.get('email', default='')
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


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
        
    user.save()

    return render(request, template)


def activation_email_confirmation(request):
    user_registered.send(AccountRegistrationForm, instance=request.user)
    messages.success(request, f"Activation email letter was sent")
    return redirect(reverse_lazy("accounts:profile"))


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_redirect_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('index')


class AccountLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


@login_required
def account_profile_view(request):
    return render(request, 'accounts/profile.html', context={"email": request.user.email})


class AccountUpdateProfileView(LoginRequiredMixin, UpdateView):
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

    def form_valid(self, form):
        messages.success(self.request, "Profile updated")
        return super(AccountUpdateProfileView, self).form_valid(form)
