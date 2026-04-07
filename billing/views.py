from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import os
from decimal import Decimal

from .models import Customer, Product, Invoice, InvoiceItem
from .forms import CustomerForm, ProductForm, InvoiceForm, InvoiceItemFormSet, ReportForm


def home(request):
    """Home page view"""
    return render(request, 'billing/home.html')


# Customer CRUD Views
def customer_list(request):
    search = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search:
        customers = customers.filter(
            Q(name__icontains=search) | 
            Q(gst_number__icontains=search)
        )
    
    context = {
        'customers': customers,
        'search': search,
    }
    return render(request, 'billing/customer_list.html', context)


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'billing/customer_form.html', {'form': form})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'billing/customer_form.html', {'form': form, 'customer': customer})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')
    
    return render(request, 'billing/customer_confirm_delete.html', {'customer': customer})


# Product CRUD Views
def product_list(request):
    search = request.GET.get('search', '')
    products = Product.objects.all()
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(hsn_code__icontains=search)
        )
    
    context = {
        'products': products,
        'search': search,
    }
    return render(request, 'billing/product_list.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'billing/product_form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'billing/product_form.html', {'form': form, 'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    return render(request, 'billing/product_confirm_delete.html', {'product': product})


# Invoice Views
def invoice_list(request):
    search = request.GET.get('search', '')
    invoices = Invoice.objects.all()
    
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) | 
            Q(customer__name__icontains=search)
        )
    
    context = {
        'invoices': invoices,
        'search': search,
    }
    return render(request, 'billing/invoice_list.html', context)


def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            
            # Save formset items
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice
                item.save()
            
            # Calculate taxes and save
            invoice.calculate_taxes()
            invoice.save()
            
            messages.success(request, 'Invoice created successfully!')
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    
    return render(request, 'billing/invoice_form.html', {
        'form': form,
        'formset': formset,
    })


def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
        
        if form.is_valid() and formset.is_valid():
            # Save form
            form.save()
            
            # Delete old items and save new ones
            invoice.items.all().delete()
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice
                item.save()
            
            # Calculate taxes and save
            invoice.calculate_taxes()
            invoice.save()
            
            messages.success(request, 'Invoice updated successfully!')
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    
    return render(request, 'billing/invoice_form.html', {
        'form': form,
        'formset': formset,
        'invoice': invoice,
    })


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully!')
        return redirect('invoice_list')
    
    return render(request, 'billing/invoice_confirm_delete.html', {'invoice': invoice})


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})


def generate_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Company info
    company_info = {
        'name': 'VIDHIM ENTERPRISES',
        'address': 'FIRST FLOOR, 105, BHAURAO UDYOG NAGAR, KHARIGAON , ABOVE S K STEEL, BHAYANDER (E)-401105',
        'phone': '+91 9892352600',
        'email': 'vidhimenterprises@gmail.com',
        'gst_no': '27AXVPS9856J1Z4'
    }
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("TAX INVOICE", title_style))
    
    # Company and Customer Info Table
    company_data = [
        [Paragraph(f"<b>{company_info['name']}</b>", styles['Normal']), 
         Paragraph(f"<b>Bill To:</b>", styles['Normal'])],
        [company_info['address'], invoice.customer.name],
        [f"Phone: {company_info['phone']}", invoice.customer.address],
        [f"Email: {company_info['email']}", f"GST: {invoice.customer.gst_number}"],
        [f"GST: {company_info['gst_no']}", ""],
    ]
    
    company_table = Table(company_data, colWidths=[3*inch, 3*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 4), (0, 4), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(company_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Invoice Details
    invoice_info = [
        ['Invoice Number:', invoice.invoice_number],
        ['Invoice Date:', invoice.invoice_date.strftime('%d-%m-%Y')],
    ]
    
    invoice_table = Table(invoice_info, colWidths=[1.5*inch, 4.5*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(invoice_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Items Table
    items_data = [['S.No', 'Product Name', 'HSN Code', 'Quantity', 'Rate', 'Total']]
    
    for i, item in enumerate(invoice.items.all(), 1):
        items_data.append([
            str(i),
            item.product.name,
            item.product.hsn_code,
            f"{item.quantity:.2f} {item.product.unit}",
            f"Rs. {item.rate:.2f}",
            f"Rs. {item.total:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Tax Calculation
    tax_data = [
        ['Subtotal:', f"Rs. {invoice.subtotal:.2f}"],
        ['CGST (2.5%):', f"Rs. {invoice.cgst:.2f}"],
        ['SGST (2.5%):', f"Rs. {invoice.sgst:.2f}"],
        ['IGST (5%):', f"Rs. {invoice.igst:.2f}"],
        ['Roundoff:', f"Rs. {invoice.roundoff:.2f}"],
        ['<b>Total:</b>', f"<b>Rs. {invoice.total:.2f}</b>"],
    ]
    
    tax_table = Table(tax_data, colWidths=[4*inch, 2*inch])
    tax_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 5), (1, 5), 'Helvetica-Bold'),
        ('FONTNAME', (0, 5), (0, 5), 'Helvetica-Bold'),
        ('LINEABOVE', (0, 5), (-1, 5), 1, colors.black),
    ]))
    story.append(tax_table)
    
    # Build PDF
    doc.build(story)
    
    # Get PDF value and return response
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
    return response


# Reports View
def reports(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            customer = form.cleaned_data['customer']
            include_fields = form.cleaned_data['include_fields']
            
            invoices = Invoice.objects.all()
            
            if start_date:
                invoices = invoices.filter(invoice_date__gte=start_date)
            if end_date:
                invoices = invoices.filter(invoice_date__lte=end_date)
            if customer:
                invoices = invoices.filter(customer=customer)
            
            # Generate PDF report
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=1
            )
            story.append(Paragraph("INVOICE REPORT", title_style))
            
            # Date Range
            if start_date and end_date:
                story.append(Paragraph(f"Period: {start_date} to {end_date}", styles['Normal']))
            elif start_date:
                story.append(Paragraph(f"From: {start_date}", styles['Normal']))
            elif end_date:
                story.append(Paragraph(f"To: {end_date}", styles['Normal']))
            
            if customer:
                story.append(Paragraph(f"Customer: {customer.name}", styles['Normal']))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Prepare data based on selected fields
            headers = [field.replace('_', ' ').title() for field in include_fields]
            data = [headers]
            
            for invoice in invoices:
                row = []
                for field in include_fields:
                    if field == 'customer':
                        row.append(invoice.customer.name)
                    elif field == 'invoice_date':
                        row.append(invoice.invoice_date.strftime('%d-%m-%Y'))
                    else:
                        row.append(str(getattr(invoice, field)))
                data.append(row)
            
            if data:
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
            
            # Build PDF
            doc.build(story)
            
            # Get PDF value and return response
            pdf = buffer.getvalue()
            buffer.close()
            
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice_report.pdf"'
            return response
    else:
        form = ReportForm()
    
    return render(request, 'billing/reports.html', {'form': form})
