# VIDHIM ENTERPRISES Billing System - Agent Instructions

## Project Overview

This is a Flask-based billing and invoicing system for VIDHIM ENTERPRISES. The main application is in `app.py`.

## How to Start the Application

### Prerequisites

- Python 3.8+
- pip package manager

### Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Key Files

| File | Description |
|------|-------------|
| `app.py` | Main Flask application (entry point) |
| `requirements.txt` | Python dependencies |
| `templates/` | HTML templates |
| `billingsys/` | Django project folder (legacy/not used) |

## Application Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/customers` | Customer list |
| `/customers/create` | Add new customer |
| `/products` | Product list |
| `/products/create` | Add new product |
| `/invoices` | Invoice list |
| `/invoices/create` | Create new invoice |
| `/invoices/<id>` | Invoice detail view |
| `/invoices/<id>/pdf` | Download invoice PDF |
| `/reports` | Generate reports |

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development mode (with debug)
python app.py

# Run tests (if any)
pytest
```

## Database

- SQLite database (`billingsys.db`)
- Automatically created on first run
- Models defined in `app.py`: Customer, Product, Invoice, InvoiceItem

## Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with Flask-SQLAlchemy
- **PDF Generation**: ReportLab 4.0.7
- **Forms**: Flask-WTF with WTForms
- **Frontend**: Bootstrap 5

## Notes

- The `manage.py` and `billingsys/` folder are from a Django version of the project (not used)
- The actual application runs via `app.py`
- The database is automatically initialized when running `python app.py`
