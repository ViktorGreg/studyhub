from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking, StudyHubSettings, Session
from .forms import BookingForm


def create_booking(request):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    settings_obj = StudyHubSettings.load()
    active_count = Session.objects.filter(status='ACTIVE').count()

    if active_count >= settings_obj.max_capacity:
        return JsonResponse({
            'success': False,
            'errors': {'capacity': ['Study hub is currently full. Please try again later.']}
        }, status=400)

    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save()
        return JsonResponse({
            'success': True,
            'booking': {
                'code': booking.booking_code,
                'guest_name': booking.guest_name,
                'plan_name': booking.plan.name,
                'duration_hours': booking.duration_hours,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)