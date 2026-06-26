from django.contrib import admin
from .models import LostTable

@admin.register(LostTable)
class LostTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'is_returned', 'found_date')

    list_filter = ('is_returned', 'found_date', 'location')

    search_fields = ('name', 'location' 'user__username')

    list_editable = ('is_returned',)

    ordering = ('-found_date',)
