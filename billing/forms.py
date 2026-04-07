from django import forms
from django.core.validators import RegexValidator
from .models import Customer, Product, Invoice, InvoiceItem


class CustomerForm(forms.ModelForm):
    gst_number = forms.CharField(
        validators=[RegexValidator(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}Z[0-9]{1}$', 'Invalid GST number format')]
    )

    class Meta:
        model = Customer
        fields = ['name', 'address', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'hsn_code', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hsn_code': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'rate']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True
)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'invoice_date', 'customer', 'tax_type']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'tax_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ReportForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False,
        empty_label="All Customers",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    include_fields = forms.MultipleChoiceField(
        choices=[
            ('invoice_number', 'Invoice Number'),
            ('invoice_date', 'Invoice Date'),
            ('customer', 'Customer'),
            ('subtotal', 'Subtotal'),
            ('cgst', 'CGST'),
            ('sgst', 'SGST'),
            ('igst', 'IGST'),
            ('roundoff', 'Roundoff'),
            ('total', 'Total'),
        ],
        initial=['invoice_number', 'invoice_date', 'customer', 'total'],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
