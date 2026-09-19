from django.core.management.base import BaseCommand
from apps.users.models import Account


class Command(BaseCommand):
    help = "Creates or resets the admin account"

    def handle(self, *args, **options):
        account, created = Account.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Super',
                'last_name': 'Admin',
                'phone_num': '+63 900 000 0000',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        account.set_password('admin12345')
        account.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Admin account created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin password reset.'))