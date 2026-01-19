# Admin Login Credentials

## Quick Access

**Admin Login URL:** http://localhost:8000/admin-login/

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

## Important Notes

⚠️ **Security Warning:** Change the default password immediately in production!

## Setup Admin User

If you need to reset or create the admin user, run:

```bash
python manage.py setup_admin
```

This will:
- Create an admin user if it doesn't exist
- Set the password to `admin123`
- Grant staff and superuser privileges

## Admin Dashboard Features

Once logged in, you'll have access to:

1. **Dashboard** - System overview with statistics
2. **Users** - Manage all registered students
3. **Detections** - View all detection results
4. **Exercises** - Manage training exercises

## Creating Additional Admins

To create more admin users:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

## Troubleshooting

### Can't Login?
1. Run `python manage.py setup_admin` to reset credentials
2. Make sure you're using `/admin-login/` not `/admin/`
3. Check that the server is running

### Forgot Password?
Run the setup command again:
```bash
python manage.py setup_admin
```

This will reset the password to `admin123`.
