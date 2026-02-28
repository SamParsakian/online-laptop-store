# app/routes/products.py
from flask import Blueprint, abort, render_template

from data.product_images import get_images_for_product
from data.products_data import get_all_products, get_product

bp = Blueprint("products", __name__)


@bp.get("/products")
def list_products():
    products = get_all_products()
    return render_template("products.html", products=products)


@bp.get("/product/<int:product_id>")
def product_details(product_id):
    product = get_product(product_id)
    if not product:
        abort(404)
    images = get_images_for_product(product_id)
    return render_template("product.html", product=product, images=images)
