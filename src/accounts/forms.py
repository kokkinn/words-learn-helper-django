from django import forms
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
        # help_text=password_validation.password_validators_help_text_html,
        # validators=[validate_password]
    )
    password2 = forms.CharField(
        label='Confirm password:',
        widget=forms.PasswordInput,
        # help_text='Please repeat password',
        # validators=[validate_password]
    )

    #
    def clean_email(self):

        print(f"CLEAN MAIL\n{self.cleaned_data}\n")
        if CustomUser.objects.filter(email=f"{self.cleaned_data['email']}"):
            raise ValidationError(message="User with this Email is registered")
        else:
            return self.cleaned_data["email"]

    #
    def clean_password1(self):
        print(f"CLEAN PW1\n{self.cleaned_data}\n")
        pwd = self.cleaned_data['password1']

        password_validation.validate_password(pwd)

        return self.cleaned_data["password1"]

    def clean(self):
        super().clean()
        # if any(self.errors):
        #     return self.errors
        # errors = []
        # if CustomUser.objects.filter(email=f"{self.cleaned_data['email']}"):
        #     errors.append(ValidationError(message="User with this Email is registered"))
        #
        # pwd = self.cleaned_data['password1']
        # if len(pwd) < 3:
        #     print("\nRaised\n")
        #     errors.append(ValidationError(message="Niga password 2 short"))
        #
        # for error in errors:
        #     raise error
        print(f"\n{self.cleaned_data}\n")

        # if CustomUser.objects.filter(email=f"{self.cleaned_data['email']}"):
        #     raise ValidationError(message="Email already registered")

        # if password_validation.validate_password(pwd)
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


class CustomAuthenticationForm(AuthenticationForm):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    # print("\nOWEGOJRWGOJEROGEROJRJ:VEVH\n")

    # def confirm_login_allowed(self, user):
    #     print("\nwpirjgi0erghoetohrtouhogurtegourtou\n")
        # if not user.is_activated:
        #     raise ValidationError(
        #         message="This user is not activated"
        #     )


class ActivationEmailConfirmationForm(forms.Form):
    email = forms.CharField()

    def __init__(self, request):
        super().__init__()
        print(str(request.user.email))
        self.fields["email"].initial = request.user.email
