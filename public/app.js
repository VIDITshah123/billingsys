// API Base URL
const API_BASE = '/api';

// Global state
let currentUser = null;

// DOM Elements
const loginScreen = document.getElementById('loginScreen');
const mainApp = document.getElementById('mainApp');
const loading = document.getElementById('loading');
const contentArea = document.getElementById('contentArea');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupEventListeners();
});

function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Navigation
    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = e.target.closest('[data-page]').dataset.page;
            navigateTo(page);
        });
    });
    
    // Logout
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
}

function checkAuth() {
    const token = localStorage.getItem('authToken');
    if (token) {
        currentUser = JSON.parse(localStorage.getItem('currentUser'));
        showMainApp();
        navigateTo('dashboard');
    } else {
        showLoginScreen();
    }
}

function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showLoginScreen() {
    loginScreen.classList.remove('d-none');
    mainApp.classList.add('d-none');
}

function showMainApp() {
    loginScreen.classList.add('d-none');
    mainApp.classList.remove('d-none');
}

async function handleLogin(e) {
    e.preventDefault();
    showLoading();
    
    const userid = document.getElementById('userid').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userid, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            localStorage.setItem('authToken', 'dummy-token');
            localStorage.setItem('currentUser', JSON.stringify({ userid }));
            currentUser = { userid };
            showMainApp();
            navigateTo('dashboard');
        } else {
            document.getElementById('loginError').textContent = data.message;
            document.getElementById('loginError').classList.remove('d-none');
        }
    } catch (error) {
        console.error('Login error:', error);
        document.getElementById('loginError').textContent = 'Login failed. Please try again.';
        document.getElementById('loginError').classList.remove('d-none');
    } finally {
        hideLoading();
    }
}

function handleLogout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    currentUser = null;
    showLoginScreen();
}

function navigateTo(page) {
    // Update active nav
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // Load page content
    switch(page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'customers':
            loadCustomers();
            break;
        case 'products':
            loadProducts();
            break;
        case 'invoices':
            loadInvoices();
            break;
        case 'reports':
            loadReports();
            break;
        default:
            loadDashboard();
    }
}

async function loadDashboard() {
    contentArea.innerHTML = `
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Dashboard</h1>
        </div>
        
        <div class="row">
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-primary shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                    Total Customers</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalCustomers">-</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-users fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-success shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                    Total Products</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalProducts">-</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-box fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-info shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                    Total Invoices</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalInvoices">-</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-file-invoice fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-warning shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                    Total Revenue</div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalRevenue">-</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-rupee-sign fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-lg-8">
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold">Recent Invoices</h6>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-bordered" id="recentInvoicesTable">
                                <thead>
                                    <tr>
                                        <th>Invoice #</th>
                                        <th>Customer</th>
                                        <th>Date</th>
                                        <th>Amount</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="4" class="text-center">Loading...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold">Quick Actions</h6>
                    </div>
                    <div class="card-body">
                        <div class="list-group">
                            <a href="#" class="list-group-item list-group-item-action" onclick="navigateTo('customers')">
                                <i class="fas fa-plus me-2"></i> Add Customer
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="navigateTo('products')">
                                <i class="fas fa-plus me-2"></i> Add Product
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="navigateTo('invoices')">
                                <i class="fas fa-plus me-2"></i> Create Invoice
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="navigateTo('reports')">
                                <i class="fas fa-chart-bar me-2"></i> View Reports
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    loadDashboardData();
}

async function loadDashboardData() {
    try {
        const [customers, products, invoices] = await Promise.all([
            fetch(`${API_BASE}/customers`).then(r => r.json()),
            fetch(`${API_BASE}/products`).then(r => r.json()),
            fetch(`${API_BASE}/invoices`).then(r => r.json())
        ]);
        
        document.getElementById('totalCustomers').textContent = customers.length;
        document.getElementById('totalProducts').textContent = products.length;
        document.getElementById('totalInvoices').textContent = invoices.length;
        
        const totalRevenue = invoices.reduce((sum, inv) => sum + inv.total, 0);
        document.getElementById('totalRevenue').textContent = `₹${totalRevenue.toLocaleString('en-IN')}`;
        
        // Load recent invoices
        const recentInvoicesTable = document.getElementById('recentInvoicesTable').getElementsByTagName('tbody')[0];
        recentInvoicesTable.innerHTML = '';
        
        invoices.slice(0, 5).forEach(invoice => {
            const row = recentInvoicesTable.insertRow();
            row.innerHTML = `
                <td>${invoice.invoice_number}</td>
                <td>${invoice.customer_name}</td>
                <td>${new Date(invoice.invoice_date).toLocaleDateString('en-IN')}</td>
                <td>₹${invoice.total.toLocaleString('en-IN')}</td>
            `;
        });
        
    } catch (error) {
        console.error('Dashboard data error:', error);
    }
}

async function loadCustomers() {
    contentArea.innerHTML = `
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Customers</h1>
            <button class="btn btn-primary" onclick="showAddCustomerModal()">
                <i class="fas fa-plus me-2"></i>Add Customer
            </button>
        </div>
        
        <div class="card shadow">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>GST Number</th>
                                <th>Address</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="customersTableBody">
                            <tr>
                                <td colspan="4" class="text-center">Loading...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
    
    try {
        const customers = await fetch(`${API_BASE}/customers`).then(r => r.json());
        const tbody = document.getElementById('customersTableBody');
        tbody.innerHTML = '';
        
        customers.forEach(customer => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${customer.name}</td>
                <td>${customer.gst_number}</td>
                <td>${customer.address}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1">Edit</button>
                    <button class="btn btn-sm btn-danger">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        console.error('Customers error:', error);
    }
}

async function loadProducts() {
    contentArea.innerHTML = `
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Products</h1>
            <button class="btn btn-primary" onclick="showAddProductModal()">
                <i class="fas fa-plus me-2"></i>Add Product
            </button>
        </div>
        
        <div class="card shadow">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>HSN Code</th>
                                <th>Unit</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="productsTableBody">
                            <tr>
                                <td colspan="4" class="text-center">Loading...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
    
    try {
        const products = await fetch(`${API_BASE}/products`).then(r => r.json());
        const tbody = document.getElementById('productsTableBody');
        tbody.innerHTML = '';
        
        products.forEach(product => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.hsn_code}</td>
                <td>${product.unit}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1">Edit</button>
                    <button class="btn btn-sm btn-danger">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        console.error('Products error:', error);
    }
}

async function loadInvoices() {
    contentArea.innerHTML = `
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Invoices</h1>
            <button class="btn btn-primary" onclick="showCreateInvoiceModal()">
                <i class="fas fa-plus me-2"></i>Create Invoice
            </button>
        </div>
        
        <div class="card shadow">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Invoice #</th>
                                <th>Customer</th>
                                <th>Date</th>
                                <th>Total</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="invoicesTableBody">
                            <tr>
                                <td colspan="5" class="text-center">Loading...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
    
    try {
        const invoices = await fetch(`${API_BASE}/invoices`).then(r => r.json());
        const tbody = document.getElementById('invoicesTableBody');
        tbody.innerHTML = '';
        
        invoices.forEach(invoice => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${invoice.invoice_number}</td>
                <td>${invoice.customer_name}</td>
                <td>${new Date(invoice.invoice_date).toLocaleDateString('en-IN')}</td>
                <td>₹${invoice.total.toLocaleString('en-IN')}</td>
                <td>
                    <button class="btn btn-sm btn-primary me-1" onclick="viewInvoice(${invoice.id})">View</button>
                    <button class="btn btn-sm btn-success me-1">PDF</button>
                    <button class="btn btn-sm btn-danger">Delete</button>
                </td>
            `;
        });
    } catch (error) {
        console.error('Invoices error:', error);
    }
}

function loadReports() {
    contentArea.innerHTML = `
        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
            <h1 class="h2">Reports</h1>
        </div>
        
        <div class="card shadow">
            <div class="card-header">
                <h6 class="m-0 font-weight-bold">Generate Report</h6>
            </div>
            <div class="card-body">
                <form id="reportForm">
                    <div class="row">
                        <div class="col-md-6">
                            <label for="startDate" class="form-label">Start Date</label>
                            <input type="date" class="form-control" id="startDate">
                        </div>
                        <div class="col-md-6">
                            <label for="endDate" class="form-label">End Date</label>
                            <input type="date" class="form-control" id="endDate">
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-12">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-chart-bar me-2"></i>Generate Report
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.getElementById('reportForm').addEventListener('submit', generateReport);
}

function generateReport(e) {
    e.preventDefault();
    alert('Report generation will be implemented with backend integration');
}

function viewInvoice(invoiceId) {
    alert(`Viewing invoice ${invoiceId} - Full implementation requires backend integration`);
}

function showAddCustomerModal() {
    alert('Add Customer modal - Full implementation requires backend integration');
}

function showAddProductModal() {
    alert('Add Product modal - Full implementation requires backend integration');
}

function showCreateInvoiceModal() {
    alert('Create Invoice modal - Full implementation requires backend integration');
}
