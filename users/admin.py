from django.contrib import admin
# from django.contrib.sessions.models import Session

from users.models import User


# class SessionAdmin(admin.ModelAdmin):
#     list_display = ('session_key', 'session_data', 'expire_date')

#     def session_data(self, obj):
#         # Декодируем данные сессии
#         return obj.get_decoded()


# admin.site.register(Session, SessionAdmin)

@admin.register(User)
class UserList(admin.ModelAdmin):
    ...
    list_display = ['id', '__str__', 'is_active', 'password']
    # readonly_fields = ('updated_at', 'created_at',)
