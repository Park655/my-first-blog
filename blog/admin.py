from django.contrib import admin
from .models import Post, Supplement, UserProfile, EffectCategory

admin.site.register(Post)

@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'effect', 'side_effect', 'note')
    filter_horizontal = ['categories']

admin.site.register(UserProfile)
admin.site.register(EffectCategory)