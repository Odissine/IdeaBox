from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display += ('last_login',)  # don't forget the commas
UserAdmin.list_filter += ('last_login',)
UserAdmin.fieldsets += ('last_login',)