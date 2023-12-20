from django.contrib import admin
from .models import BotUser, Feedback
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'user_id', 'created_at', 'subscribed']


admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Feedback)
