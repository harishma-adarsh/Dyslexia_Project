from django.contrib.auth.models import User

# Get or create admin user
try:
    admin = User.objects.get(username='admin')
    print(f"Admin user found: {admin.username}")
except User.DoesNotExist:
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created")

# Set password
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()

print(f"Admin password set to: admin123")
print(f"Is staff: {admin.is_staff}")
print(f"Is superuser: {admin.is_superuser}")
print("\nYou can now login at /admin-login/ with:")
print("Username: admin")
print("Password: admin123")
