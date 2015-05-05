from django.contrib import admin
from .models import UserProfile
from django.db.models.signals import post_save, post_delete


def _clear_cache(**kwargs):
    """Clear the cache when a UserProfile is added or removed
    This is to make sure that we remove the information from the page
    as well
    """
    print 'CACHE CLEARED'
    pass


post_save.connect(_clear_cache, sender=UserProfile)
post_delete.connect(_clear_cache, sender=UserProfile)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['name', 'major']
    list_display = ('__str__', 'is_registered')
