from django.contrib import admin
from .models import User, Friend, Prize, Winning
from .models import Card
from .models import GameSession



class FriendInline(admin.StackedInline):
    model = Friend
    extra = 5


class UserAdmin(admin.ModelAdmin):
    inlines = [FriendInline]


admin.site.register(User, UserAdmin)
admin.site.register(Friend)
admin.site.register(Prize)
admin.site.register(Winning)
admin.site.register(Card)
admin.site.register(GameSession)