from django.contrib import admin

# Register your models here.
from .models import Booking, RegisteredUser, Contacted


class BookingSettingsAdmin(admin.ModelAdmin):
    model = Booking
    readonly_fields = (
        'id',
    )

admin.site.register(Booking, BookingSettingsAdmin)
admin.site.register(RegisteredUser)
admin.site.register(Contacted)
