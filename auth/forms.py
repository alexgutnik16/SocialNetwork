from django import forms


class PhoneCreationForm(forms.Form):
    phone = forms.CharField(max_length=20, required=True, help_text='Phone number')


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')