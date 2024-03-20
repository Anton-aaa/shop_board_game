from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy
from myapp.models import MyUser, Purchase, ReturnGoods


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=("Enter the same password as above for verification."))

    class Meta:
        model = MyUser
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.wallet = 1000
            user.save()
        return user


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['purchase_quantity']


# class ReturnGoodsForm(ModelForm):
#     class Meta:
#         model = ReturnGoods