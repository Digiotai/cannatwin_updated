from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            field_names = [field_name for field_name, _ in self.fields.items()]
            for field_name in field_names:
                field = self.fields.get(field_name)
                field.widget.attrs.update({'placeholder': field.label})
        except Exception as e:
            print(e)


class CreateUserForm(PlaceholderMixin, ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        try:
            model = User

            fields = ['username', 'email', 'password']
            # exclude = ('password1','password2')
        except Exception as e:
            print(e)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields.pop("password1", None)
    #     self.fields.pop("password2", None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user
