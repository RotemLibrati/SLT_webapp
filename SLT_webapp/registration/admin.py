from django.contrib import admin
from .models import User
from .models import GameSession



"""class FriendInline(admin.StackedInline):
    model = Friend
    extra = 5

class UserAdmin(admin.ModelAdmin):
    inlines = [FriendInline]"""

admin.site.register(User)
admin.site.register(GameSession)