from django.contrib import admin
from .models import Item, Supplier, Client, SupplierOrder, StockIssue, PaymentRecord


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "quantity", "status", "reorder_level")
    list_filter = ("status", "category")
    search_fields = ("name", "category")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "contact_person", "phone", "email")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone")
    search_fields = ("name", "contact_person", "phone", "email")


@admin.register(SupplierOrder)
class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "item", "quantity_ordered", "status", "ordered_at")
    list_filter = ("status", "supplier")
    search_fields = ("supplier__name", "item__name")


@admin.register(StockIssue)
class StockIssueAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "client", "quantity", "issue_date")
    list_filter = ("issue_date",)
    search_fields = ("item__name", "client__name", "issued_by")


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "method", "amount", "status", "created_at")
    list_filter = ("method", "status")
    search_fields = ("reference", "phone_number")
