from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class AccountRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirm password:',
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        if CustomUser.objects.filter(email=f"{self.cleaned_data['email']}"):
            raise ValidationError(message="User with this Email is registered")
        else:
            return self.cleaned_data["email"]

    def clean_password1(self):
        pwd = self.cleaned_data['password1']
        password_validation.validate_password(pwd)
        return self.cleaned_data["password1"]

    def clean(self):
        super().clean()

        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError(
                {
                    'password2': ValidationError('Password not equals', code='password_mismatch')
                }
            )
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = False
        if commit:
            user.save()
        messages.success(self.request, "You've successfully registered!")
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class AccountUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if not self.request.user.is_activated:
            self.fields["username"].disabled = True
            self.fields["first_name"].disabled = True
            self.fields["last_name"].disabled = True
            self.fields["birthday"].disabled = True
            self.fields["city"].disabled = True
            self.fields["avatar"].disabled = True

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'city',
            'avatar',
        ]


class ActivationEmailConfirmationForm(forms.Form):
    email = forms.CharField()

    def __init__(self, request):
        super().__init__()
        print(str(request.user.email))
        self.fields["email"].initial = request.user.email
