from django import forms
from .models import Booking, StudyHubPlan


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_phone', 'plan', 'duration_hours', 'wants_locker']