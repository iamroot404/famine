from django.contrib import admin
from .models import Donation, Amount, Items, Area

# Register your models here.
class DonationAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'amount', 'transaction_id')

class ItemsAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'item', 'quantity')

class AreaAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'region', 'county', 'country')


admin.site.register(Area, AreaAdmin)

admin.site.register(Items, ItemsAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Amount)