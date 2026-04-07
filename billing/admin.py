from django.contrib import admin
from .models import Customer, Product, Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['product', 'quantity', 'rate', 'total']
    readonly_fields = ['total']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'gst_number', 'created_at']
    search_fields = ['name', 'gst_number']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'hsn_code', 'unit', 'created_at']
    search_fields = ['name', 'hsn_code']
    list_filter = ['unit', 'created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'invoice_date', 'total', 'created_at']
    search_fields = ['invoice_number', 'customer__name']
    list_filter = ['invoice_date', 'tax_type', 'created_at']
    inlines = [InvoiceItemInline]
    readonly_fields = ['subtotal', 'cgst', 'sgst', 'igst', 'roundoff', 'total']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_taxes()
        obj.save()


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'product', 'quantity', 'rate', 'total']
    search_fields = ['invoice__invoice_number', 'product__name']
