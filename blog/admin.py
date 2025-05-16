from django.contrib import admin
from .models import Post, Supplement

admin.site.register(Post)

@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'effect', 'side_effect', 'note')