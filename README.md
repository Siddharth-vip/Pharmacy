# Pharmacy Web Application (Django & Tailwind CSS)

An e-commerce pharmacy web application built with **Django** (Backend & Templating) and **Tailwind CSS** (Frontend styling).

---

## 🚀 Quick Start - Running the Application

### 1. Start the Django Server
Run this terminal command in the project root directory:

```bash
python manage.py runserver
```

Once running, access the web application in your browser:
- **Frontend / Home:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### 2. (Optional) Run Tailwind CSS Live Compiler
If you modify Tailwind CSS classes in templates or config files:

```bash
npm run dev
```

---

## 📦 Installed Dependencies & Requirements

### Python Dependencies
- **Django** (`>=5.1.0,<5.2.0`) - Web framework
- **Pillow** (`>=10.0.0`) - Image handling for product & user image fields
- **asgiref** (`>=3.8.1`) - ASGI specifications and helper functions
- **sqlparse** (`>=0.5.0`) - Non-validating SQL parser
- **tzdata** - Time zone data support

To reinstall Python dependencies at any time:
```bash
pip install -r requirements.txt
```

### Node.js Dependencies
- **tailwindcss** (`^3.4.16`)
- **postcss** (`^8.4.49`)
- **autoprefixer** (`^10.4.20`)

To reinstall Node dependencies:
```bash
npm install
```

---

## 🛠 Project Architecture & Features

### Applications & Modules:
- **`app/`**: Core application managing users, products, cart items, categories, and views.
  - **Models**:
    - `CustomUser`: Profile extension with contact number, address, and profile image.
    - `Product`: Medicine/pharmacy items with price, stock, ratings, benefits, usage, precautions, and categories.
    - `Category`: Categorization for pharmacy products.
    - `Cart` & `CartItem`: Shopping cart and quantity management with dynamic AJAX updates.
  - **Views & Routes**:
    - Authentication (`/users/register`, `/users/login`, `/users/logout`, `/users/edit_profile`)
    - Catalog & Search (`/products/`, `/products/<id>`, `/products/search/`)
    - Cart & Checkout (`/products/cart/`, `/products/buynow/`)
    - Static Pages (`/users/about`, `/users/contact`, `/users/helpsupport`)
- **`project/`**: Django project settings, ASGI/WSGI configs, and root URL routing.
- **`templates/`**: HTML templates with responsive UI layouts.
- **`static/`**: Compiled CSS, custom JavaScript, and asset files.
- **`media/`**: Uploaded user and product media.

---

## 🔧 Useful Management Commands

- **Apply Database Migrations:**
  ```bash
  python manage.py migrate
  ```

- **Create an Admin Superuser:**
  ```bash
  python manage.py createsuperuser
  ```
