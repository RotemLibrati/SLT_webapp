from django.contrib import admin
from .models import UserProfile, Friend, Prize, Winning
from .models import Card
from .models import GameSession,UserReoprt


admin.site.register(UserProfile)
admin.site.register(Friend)
admin.site.register(Prize)
admin.site.register(Winning)
admin.site.register(Card)
admin.site.register(GameSession)
admin.site.register(UserReoprt)