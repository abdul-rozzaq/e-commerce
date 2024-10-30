from typing import Any

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            try:
                self.user_cache = User.objects.get(email=email)

                if not self.user_cache.check_password(password):
                    raise self.get_invalid_login_error()

                self.confirm_login_allowed(self.user_cache)

            except User.DoesNotExist:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("User holati active emas.", code="inactive")

    def get_invalid_login_error(self):
        return ValidationError("User topilmadi. Email yoki parol xato.", code="invalid_login")
