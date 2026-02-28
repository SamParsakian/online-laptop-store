# Online Laptop Store

A simple Flask web app for browsing and purchasing laptops (student project).

## Setup

1. **Create and activate a virtual environment** (from the project root):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Optional — environment variables**: Copy `.env.example` to `.env` and set `SECRET_KEY`, `ADMIN_USER`, and `ADMIN_PASS` if you want to override defaults.

## Run

From the project root (`online-laptop-store/`):

```bash
python -m app.app
```

Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser. You should see the home page.
