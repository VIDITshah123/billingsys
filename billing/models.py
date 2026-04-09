from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    gst_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', 'Invalid GST number format')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Product(models.Model):
    UNIT_CHOICES = [
        ('kgs', 'Kilograms'),
        ('units', 'Units'),
    ]

    name = models.CharField(max_length=200)
    hsn_code = models.CharField(max_length=8)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ['-created_at']


class Invoice(models.Model):
    TAX_TYPE_CHOICES = [
        ('cgst_sgst', 'CGST + SGST'),
        ('igst', 'IGST'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES, default='cgst_sgst')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_taxes(self):
        """Calculate taxes based on invoice items"""
        items = self.items.all()
        if not items:
            return

        # Calculate taxable value (subtotal)
        self.subtotal = sum(item.quantity * item.rate for item in items)
        
        # Calculate taxes
        if self.tax_type == 'cgst_sgst':
            self.cgst = self.subtotal * Decimal('0.025')  # 2.5%
            self.sgst = self.subtotal * Decimal('0.025')  # 2.5%
            self.igst = Decimal('0')
        else:  # IGST
            self.igst = self.subtotal * Decimal('0.05')   # 5%
            self.cgst = Decimal('0')
            self.sgst = Decimal('0')

        # Calculate roundoff
        total_before_roundoff = self.subtotal + self.cgst + self.sgst + self.igst
        decimal_part = total_before_roundoff - int(total_before_roundoff)
        self.roundoff = Decimal('1') if decimal_part >= Decimal('0.5') else Decimal('0')

        # Calculate total
        self.total = self.subtotal + self.cgst + self.sgst + self.igst + self.roundoff

    def __str__(self):
        return f"Invoice {self.invoice_number}"

    class Meta:
        ordering = ['-created_at']


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.rate
        super().save(*args, **kwargs)
        # Recalculate invoice totals when item is saved
        self.invoice.calculate_taxes()
        self.invoice.save()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} @ {self.rate}"
