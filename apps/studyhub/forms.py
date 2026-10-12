from django import forms
from .models import Booking, StudyHubPlan, StudyHubSettings, Session


class BookingForm(forms.ModelForm):
  class Meta:
    model = Booking
    fields = ['guest_name', 'guest_phone', 'plan', 'duration_hours', 'wants_locker']

class SessionForm(forms.ModelForm):
  class Meta:
    model = Session
    fields = ['booking']

class SettingsForm(forms.ModelForm):
  class Meta:
    model = StudyHubSettings
    fields = ['max_capacity', 'max_lockers']