from django.contrib import admin

from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'seats', 'location', 'get_reservations_count')
    search_fields = ('name', 'location')
    list_filter = ('seats',)

    def get_reservations_count(self, obj):
        return obj.reservations.count()
    get_reservations_count.short_description = 'Количество броней'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'reservation',
        'duration',
    )
    list_filter = ('table', 'reservation')
    search_fields = ('customer', 'table__name')
    date_hierarchy = 'reservation'
