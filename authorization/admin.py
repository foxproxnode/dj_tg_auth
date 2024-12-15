from django.contrib import admin
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')

    def session_data(self, obj):
        return obj.get_decoded()


admin.site.register(Session, SessionAdmin)
