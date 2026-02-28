# Online Laptop Store

A simple Flask web app for browsing and purchasing laptops (student project). Built with Flask, SQLite, and Bootstrap.

## Features

- **Public:** Home page with hero and featured products, product list and detail pages, add to cart, view cart, remove items, checkout with customer details, order confirmation (no real payment).
- **Admin:** Login-protected panel; manage products (CRUD) and product images; view and update order status (PENDING / PROCESSING / SHIPPED); view and approve payments; create additional admin users.
- **Tech:** SQLite database, session-based cart and admin auth, responsive UI.

## Project structure

```
online-laptop-store/
├── app/
│   ├── app.py              # Flask app, routes registration, home, admin gate, 404
│   ├── routes/
│   │   ├── products.py     # /products, /product/<id>
│   │   ├── cart.py         # /cart, /cart/add/<id>, /cart/remove/<id>, /checkout
│   │   ├── payment.py      # /buy/confirm (POST), /buy/<id> (GET, no UI link)
│   │   └── admin.py        # /admin/* (login, dashboard, products, orders, payments, new admin)
│   ├── templates/
│   └── static/             # css, js, img
├── data/
│   ├── database.py         # get_connection, init_db (schema + seed + admin sync)
│   ├── schema.sql
│   ├── seed.sql            # 17 products, product images
│   ├── products_data.py
│   ├── product_images.py
│   └── orders_data.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone or download** the project and go to the project root.

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Optional — environment variables:**  
   Copy `.env.example` to `.env` and adjust if needed. If you skip this, the app uses defaults (see below).

## Run

From the project root:

```bash
python -m app.app
```

Then open **http://127.0.0.1:5000/** in your browser.

## Environment variables

| Variable     | Purpose           | Default   |
|-------------|-------------------|-----------|
| `SECRET_KEY` | Flask session key | `change-me` |
| `ADMIN_USER` | Admin login name  | `admin`  |
| `ADMIN_PASS` | Admin password    | `1234`   |

The first time the app runs, it creates the SQLite database and seed data (if the database is empty). The admin user is created or updated from these env values.

## Admin login

- **URL:** http://127.0.0.1:5000/admin  
- **Default credentials:** username `admin`, password `1234` (unless set in `.env`).

After login you can manage products, product images, orders, payments, and create more admin users.

---

## Manual test checklist

Use this to verify the app before pushing or demoing.

### Public flows

- [ ] **Home:** Open `/`. See hero (“Find Your Next Laptop”), intro text, trust points, “Browse All Products” button, and a “Featured Products” section with a few cards.
- [ ] **Product list:** Click “Browse All Products” or “Products”. See a grid of product cards (image, name, type, price, “Details”). Layout is responsive (e.g. 1 column on small screens).
- [ ] **Product detail:** Click “Details” on a product. See specs, one or more product images (sized reasonably), “Add to Cart” and “Back to List”. Click “Add to Cart” — you are redirected back to the same product page.
- [ ] **Cart:** Open “Cart” in the nav. See items (name, price, quantity, line total) and “Remove” per line. Remove one item and confirm the cart updates. Use “Continue Shopping” and “Checkout” when the cart has items.
- [ ] **Checkout:** With items in cart, click “Checkout”. See order summary and a form (name, phone, address). Fill and submit “Proceed to Payment”. You should land on an order confirmation page (order ID, total, items, contact details). Cart should be empty afterward.
- [ ] **404:** Visit a non-existent URL (e.g. `/xyz`). See a “Page not found” message and a “Go Home” link.

### Admin flows

- [ ] **Login:** Go to `/admin`. Enter `admin` / `1234`. You are redirected to the admin dashboard.
- [ ] **Dashboard:** See links to Products, Orders, Payments, and Add Admin. Open each section.
- [ ] **Products:** List products. Create a new product (all fields). Edit a product. Delete a product (confirm). Open “Images” for a product: add an image URL, remove an image.
- [ ] **Orders:** List orders. Open one order: see details and line items. Change status (e.g. PENDING → PROCESSING) and submit “Update”. Confirm the status updates.
- [ ] **Payments:** List payment records. Use “Approve” on a pending payment and confirm it shows as approved.
- [ ] **New admin:** Create a second admin (username + password). Logout, then log in with the new admin.
- [ ] **Logout:** Click “Logout”. You are on the home page. Visiting `/admin/dashboard` redirects to the login page.

---

## Pushing to GitHub

- Ensure `.env` is not committed (it is in `.gitignore`).
- The database file `*.db` is ignored; each clone will get a fresh DB and seed on first run.
- After running through the checklist above, the project is ready to push as a student project.
