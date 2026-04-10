import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('billingsys.db')
    conn.row_factory = sqlite3.Row
    return conn

# Simple authentication (for demo purposes)
USERS = {"admin": "admin123"}

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return jsonify({'error': 'Authentication required'}), 401
        
        # In production, use proper JWT or session management
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    userid = data.get('userid')
    password = data.get('password')
    
    if userid in USERS and USERS[userid] == password:
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        conn = get_db_connection()
        customers = conn.execute('SELECT * FROM customers ORDER BY created_at DESC').fetchall()
        conn.close()
        
        result = []
        for customer in customers:
            result.append({
                'id': customer['id'],
                'name': customer['name'],
                'address': customer['address'],
                'gst_number': customer['gst_number'],
                'created_at': customer['created_at']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
        conn.close()
        
        result = []
        for product in products:
            result.append({
                'id': product['id'],
                'name': product['name'],
                'hsn_code': product['hsn_code'],
                'unit': product['unit'],
                'created_at': product['created_at']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    try:
        conn = get_db_connection()
        invoices = conn.execute('''
            SELECT i.*, c.name as customer_name 
            FROM invoices i 
            LEFT JOIN customers c ON i.customer_id = c.id 
            ORDER BY i.created_at DESC
        ''').fetchall()
        conn.close()
        
        result = []
        for invoice in invoices:
            result.append({
                'id': invoice['id'],
                'invoice_number': invoice['invoice_number'],
                'invoice_date': invoice['invoice_date'],
                'customer_id': invoice['customer_id'],
                'customer_name': invoice['customer_name'],
                'tax_type': invoice['tax_type'],
                'subtotal': float(invoice['subtotal']),
                'cgst': float(invoice['cgst']),
                'sgst': float(invoice['sgst']),
                'igst': float(invoice['igst']),
                'total': float(invoice['total']),
                'created_at': invoice['created_at']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    try:
        conn = get_db_connection()
        invoice = conn.execute('''
            SELECT i.*, c.name as customer_name, c.address, c.gst_number 
            FROM invoices i 
            LEFT JOIN customers c ON i.customer_id = c.id 
            WHERE i.id = ?
        ''', (invoice_id,)).fetchone()
        
        items = conn.execute('''
            SELECT ii.*, p.name as product_name, p.hsn_code, p.unit 
            FROM invoice_items ii 
            LEFT JOIN products p ON ii.product_id = p.id 
            WHERE ii.invoice_id = ?
        ''', (invoice_id,)).fetchall()
        
        conn.close()
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        invoice_data = {
            'id': invoice['id'],
            'invoice_number': invoice['invoice_number'],
            'invoice_date': invoice['invoice_date'],
            'customer': {
                'name': invoice['customer_name'],
                'address': invoice['address'],
                'gst_number': invoice['gst_number']
            },
            'tax_type': invoice['tax_type'],
            'subtotal': float(invoice['subtotal']),
            'cgst': float(invoice['cgst']),
            'sgst': float(invoice['sgst']),
            'igst': float(invoice['igst']),
            'total': float(invoice['total']),
            'items': []
        }
        
        for item in items:
            invoice_data['items'].append({
                'id': item['id'],
                'product_name': item['product_name'],
                'hsn_code': item['hsn_code'],
                'unit': item['unit'],
                'quantity': float(item['quantity']),
                'rate': float(item['rate']),
                'total': float(item['total'])
            })
        
        return jsonify(invoice_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handler for Netlify Functions
def handler(event, context):
    # This is the entry point for Netlify Functions
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
