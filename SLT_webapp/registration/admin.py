from django.contrib import admin
from .models import User, Friend, Prize, Winning


class FriendInline(admin.StackedInline):
    model = Friend
    extra = 5


class UserAdmin(admin.ModelAdmin):
    inlines = [FriendInline]


admin.site.register(User, UserAdmin)
admin.site.register(Friend)
admin.site.register(Prize)
admin.site.register(Winning)
