from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_staff')
