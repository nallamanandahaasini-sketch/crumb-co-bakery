# Crumb & Co. — Bakery Management System

A responsive Flask + MySQL bakery website and staff management portal.

## Included
- Customer registration/login, product catalogue, session basket, checkout and order history
- Role-based staff portal for admin, manager, cashier, baker and storekeeper
- Product catalogue management, order status updates, bill generation (discount + tax)
- Ingredient inventory, low-stock alerts, supplier records and date-filtered sales reports
- Bootstrap responsive storefront with bakery-themed styling

The scope follows the supplied project report: online payment gateway and mobile app are not included in this initial version.

## Setup
1. Install Python 3.10+ and MySQL.
2. Create a database:
   ```sql
   CREATE DATABASE bakery_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   ```
4. Install dependencies: `pip install -r requirements.txt`
5. Set your database connection (Windows PowerShell example):
   ```powershell
   $env:DATABASE_URL="mysql+pymysql://root:YOUR_PASSWORD@localhost/bakery_db?charset=utf8mb4"
   $env:SECRET_KEY="replace-with-a-long-random-secret"
   ```
   Or edit `config.py` for local development.
6. Create tables and sample data: `python seed.py`
7. Start: `python app.py`
8. Open `http://127.0.0.1:5000`

## Demo staff account
- Email: `admin@crumbandco.com`
- Password: `Admin@12345`

Change this password and the SECRET_KEY before deployment. Seed data is only for local demonstration.

## Roles
Set a user's `role` field to one of: `customer`, `cashier`, `baker`, `storekeeper`, `manager`, `admin`.
New public registrations are always customers. Create staff accounts from a trusted admin workflow or directly in the database.

## Project layout
- `app.py`: application factory and routes
- `models.py`: SQLAlchemy data models
- `auth.py`: authentication
- `shop.py`: customer storefront and orders
- `admin.py`: role-protected staff workflows
- `templates/`: Jinja pages
- `static/css/`, `static/js/`: styling and browser interactions

## Notes
- Payments are recorded as Cash/UPI/Card by staff; no payment gateway is integrated.
- Product images are remote Unsplash URLs; replace with locally licensed images for production.
- For production, turn off Flask debug mode, use HTTPS, configure backups, CSRF protection, rate limiting and secure cookie settings.
