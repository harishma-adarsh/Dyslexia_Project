from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Setup admin user for the system'

    def handle(self, *args, **options):
        # Get or create admin user
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write(f"Admin user found: {admin.username}")
        except User.DoesNotExist:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write("Admin user created")

        # Set password
        admin.set_password('admin123')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        self.stdout.write(self.style.SUCCESS(f"Admin password set to: admin123"))
        self.stdout.write(self.style.SUCCESS(f"Is staff: {admin.is_staff}"))
        self.stdout.write(self.style.SUCCESS(f"Is superuser: {admin.is_superuser}"))
        self.stdout.write(self.style.SUCCESS("\nYou can now login at /admin-login/ with:"))
        self.stdout.write(self.style.SUCCESS("Username: admin"))
        self.stdout.write(self.style.SUCCESS("Password: admin123"))
