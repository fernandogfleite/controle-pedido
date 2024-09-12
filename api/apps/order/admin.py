from django.contrib import admin

from api.apps.order.models.order import Table


# Register your models here.
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "status", "description")
    list_filter = ("status",)
    search_fields = ("number", "description")


admin.site.register(Table, TableAdmin)
