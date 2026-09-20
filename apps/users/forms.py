from django import forms
from .models import Account


class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_num', 'username', 'password']

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password'])  # hash it, never store raw
        account.role = 'STAFF'
        if commit:
            account.save()
        return account