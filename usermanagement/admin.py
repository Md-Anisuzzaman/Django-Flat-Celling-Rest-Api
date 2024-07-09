from django.contrib import admin
from .models import UserAccount

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id','uid','email','name','phone_number','created_at', 'updated_at')
    list_display_links = ('email',)

admin.site.register(UserAccount, UserAccountAdmin)
