import random
import string
from django.db import models
from django.conf import settings


def generate_booking_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class StudyHubSettings(models.Model):
    """Singleton, same pattern as CafeSettings — holds the seat capacity."""
    max_capacity = models.PositiveIntegerField(default=20)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Study Hub Settings (capacity: {self.max_capacity})"


class StudyHubPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_value = models.PositiveIntegerField(default=1)
    duration_unit = models.CharField(max_length=20, default='hour')  # hour, day, week, month
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]

    guest_name = models.CharField(max_length=150)
    guest_phone = models.CharField(max_length=20, blank=True)
    plan = models.ForeignKey(StudyHubPlan, on_delete=models.PROTECT)
    booking_code = models.CharField(max_length=6, unique=True, default=generate_booking_code)
    duration_hours = models.PositiveIntegerField(default=1)
    wants_locker = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest_name} — {self.booking_code}"


class Session(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sessions_started')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions_ended')
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"Session for {self.booking.guest_name}"