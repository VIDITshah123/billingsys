# Project Checklist

## 1. Inline Add for Customers and Products
- [x] **Customer List Page** (`/customers`)
  - [x] Add a new row at top/bottom of customer table with input fields:
    - [x] Name (text input)
    - [x] Address (text area)
    - [x] GST Number (text input with validation)
  - [x] Add "Add" button in that row
  - [x] On click, validate inputs and add customer inline
  - [x] Clear input fields after successful add
  - [x] Show error message if validation fails

- [x] **Product List Page** (`/products`)
  - [x] Add a new row at top/bottom of product table with input fields:
    - [x] Name (text input)
    - [x] HSN Code (text input)
    - [x] Unit (dropdown: kgs/units)
  - [x] Add "Add" button in that row
  - [x] On click, validate inputs and add product inline
  - [x] Clear input fields after successful add

## 2. Reports Page - Select All Checkbox
- [x] Add a "Select All" checkbox above the field selection checkboxes
- [x] When checked, automatically check all available fields
- [x] When unchecked, uncheck all fields
- [x] Add logic to default to all fields if no fields are selected on submit

## 3. Reports Page - Quarter and Year Buttons
- [x] Add "Q1" button (Jan 1 - Mar 31)
- [x] Add "Q2" button (Apr 1 - Jun 30)
- [x] Add "Q3" button (Jul 1 - Sep 30)
- [x] Add "Q4" button (Oct 1 - Dec 31)
- [x] Add "Year" button (Apr 1 - Mar 31 of current financial year)
- [x] On click, populate start_date and end_date fields with appropriate values
- [x] Style buttons consistently (Bootstrap buttons)

## 4. Export Report as Excel
- [x] Add "Export to Excel" button on reports page
- [x] Install required library (openpyxl)
- [x] Add route for Excel export (`/reports` with export_type parameter)
- [x] Generate Excel file with:
  - [x] Header row with field names
  - [x] Data rows with invoice information
  - [x] Proper column widths
- [x] Return Excel file as downloadable attachment

## 5. Invoice Creation - Dedicated Page
- [x] Create new invoice creation page (`/invoices/create`)
- [x] Add customer selection dropdown
- [x] Add product selection dropdown
- [x] Add quantity input field
- [x] Add rate/price input field
- [x] Add tax type selection (CGST/SGST or IGST)
- [x] Add "Add Item" button to add product to invoice
- [x] Show list of added items with delete options
- [x] Auto-calculate and display:
  - [x] Subtotal
  - [x] CGST @ 2.5% (if CGST/SGST selected)
  - [x] SGST @ 2.5% (if CGST/SGST selected)
  - [x] IGST @ 5% (if IGST selected)
  - [x] Total amount
- [x] Update tax calculations when tax type changes
- [x] Add "Create Invoice" button to save invoice

## 6. Login Page
- [x] Create login page (`/login`)
- [x] Add userid input field
- [x] Add password input field (masked)
- [x] Add "Login" button
- [x] Create default user: admin / admin123
- [x] Validate credentials against stored data
- [x] On successful login, redirect to home/dashboard
- [x] On failed login, show error message
- [x] Add route protection decorator/middleware:
  - [x] Check for valid session on all protected routes
  - [x] Redirect to login page if not authenticated
- [x] Protected routes:
  - [x] `/` (home)
  - [x] `/customers`
  - [x] `/customers/create`
  - [x] `/products`
  - [x] `/products/create`
  - [x] `/invoices`
  - [x] `/invoices/create`
  - [x] `/invoices/<id>`
  - [x] `/reports`

## 7. Login Details in JSON File
- [x] Create `users.json` file (auto-created on first run)
- [x] Store default user: `{"userid": "admin", "password": "admin123"}`
- [x] Create utility functions to:
  - [x] Load users from JSON file
  - [x] Validate credentials against JSON data
- [x] Update login route to read from JSON file
