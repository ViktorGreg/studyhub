from django import forms
from .models import CafeSettings


class CafeSettingsForm(forms.ModelForm):
    class Meta:
        model = CafeSettings
        fields = ['cafe_name', 'tagline', 'description', 'phone', 'hours', 'address']