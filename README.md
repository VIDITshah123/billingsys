# VIDHIM ENTERPRISES Billing System

A comprehensive web application for managing invoices, customers, and products for VIDHIM ENTERPRISES.

## Features

- **Customer Management**: Add, update, delete, and search customers with GST validation
- **Product Management**: Manage products with HSN codes and unit types (kgs/units)
- **Invoice Creation**: Create invoices with automatic tax calculations (CGST/SGST/IGST)
- **PDF Generation**: Generate professional PDF invoices and reports
- **Reporting System**: Filter and export invoices by date range and customer
- **Responsive Design**: Modern Bootstrap 5 interface

## Tax Calculations

- **CGST**: 2.5% of taxable value
- **SGST**: 2.5% of taxable value  
- **IGST**: 5% of taxable value
- **Roundoff**: Automatically calculated (0.50 and above rounds to 1)
- **Total**: Taxable value + CGST + SGST + IGST + Roundoff

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access Application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Company Information

- **Name**: VIDHIM ENTERPRISES
- **Address**: FIRST FLOOR, 105, BHAURAO UDYOG NAGAR, KHARIGAON , ABOVE S K STEEL, BHAYANDER (E)-401105
- **Phone**: +91 9892352600
- **Email**: vidhimenterprises@gmail.com
- **GST No**: 27AXVPS9856J1Z4

## Usage

### Managing Customers

1. Navigate to **Customers** from the navigation menu
2. Click **Add Customer** to create a new customer
3. Enter customer details including GST number (validated format)
4. Use search functionality to find specific customers

### Managing Products

1. Navigate to **Products** from the navigation menu
2. Click **Add Product** to create a new product
3. Enter product details including HSN code and unit type
4. Products can be measured in kilograms (kgs) or units

### Creating Invoices

1. Navigate to **Invoices** and click **Create New Invoice**
2. Enter invoice number and date
3. Select customer from dropdown
4. Choose tax type (CGST+SGST or IGST)
5. Add products with quantity and rate
6. Taxes are calculated automatically
7. Save and download PDF invoice

### Generating Reports

1. Navigate to **Reports** from the navigation menu
2. Filter by date range and/or customer
3. Select fields to include in the report
4. Generate and download PDF report

## Technical Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome
- **PDF Generation**: ReportLab 4.0.7
- **Forms**: Flask-WTF with WTForms

## Project Structure

```
billingsys/
    app.py                      # Main Flask application
    requirements.txt            # Python dependencies
    templates/                  # HTML templates
        base_flask.html         # Base template
        home.html               # Home page
        customer_list.html      # Customer listing
        customer_form.html      # Customer add/edit form
        product_list.html       # Product listing
        product_form.html       # Product add/edit form
        invoice_list.html       # Invoice listing
        invoice_form.html       # Invoice creation form
        invoice_detail.html     # Invoice detail view
        reports.html            # Reports generation
    billingsys.db              # SQLite database (created automatically)
```

## License

This project is proprietary to VIDHIM ENTERPRISES.
