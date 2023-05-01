from django.contrib import admin

from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    '''
    Represents a menu item on the admin site.
    '''
    list_display = [
        'name',
        'parent',
        'path',
        'position',
    ]

    list_editable = [
        'position',
    ]

    list_filter = [
        'parent',
    ]

    search_fields = [
        'name',
        'path',
    ]
