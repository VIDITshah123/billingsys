# VIDHIM ENTERPRISES Billing System

A comprehensive Flask-based billing and invoicing system for VIDHIM ENTERPRISES with customer management, product catalog, invoice generation, and reporting capabilities.

## Features

### 🏢 Company Management
- Company information management
- GST compliance for Indian businesses
- Professional invoice generation

### 👥 Customer Management
- Add, edit, and delete customers
- GST number validation
- Customer search functionality
- Inline customer addition for quick workflow

### 📦 Product Management
- Product catalog with HSN codes
- Unit-based inventory (kgs/units)
- Product search functionality
- Inline product addition

### 🧾 Invoice Management
- Create professional invoices
- Tax calculations (CGST 2.5%, SGST 2.5%, IGST 5%)
- Multiple invoice items per invoice
- PDF invoice generation with professional layout
- Invoice item management (add/delete)

### 📊 Reporting
- Generate reports by date range
- Customer-specific reports
- Export to PDF and Excel formats
- Selectable field inclusion
- Quick date range buttons (Q1, Q2, Q3, Q4, Year)

### 🔐 Authentication
- User login system
- Session management
- Protected routes
- JSON-based user storage

## Tax Calculations

The system follows Indian GST tax rules:
- **CGST**: 2.5% of subtotal
- **SGST**: 2.5% of subtotal
- **IGST**: 5% of subtotal (for inter-state transactions)
- **Total**: Subtotal + applicable taxes (rounded to nearest integer)

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/billingsys.git
   cd billingsys
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

### Default Login
- **Username**: admin
- **Password**: admin123

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
