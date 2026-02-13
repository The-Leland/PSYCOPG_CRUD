


from flask import Blueprint
from db import get_connection


from controllers import product_controller as controller

product = Blueprint('product', __name__)

@product.route('/product', methods=['POST'])
def add_product_route():
    return controller.add_product()

@product.route('/product/<product_id>', methods=['GET'])
def get_product_by_id_route(product_id):
    return controller.get_product_by_id(product_id)

@product.route('/products', methods=['GET'])
def get_all_products_route():
    return controller.get_all_products()

@product.route('/products/active', methods=['GET'])
def get_active_products_route():
    return controller.get_active_products()

@product.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id_route(product_id):
    return controller.update_product_by_id(product_id)

@product.route('/product/active/<product_id>', methods=['PATCH'])
def update_product_active_route(product_id):
    return controller.update_product_active(product_id)

@product.route('/product/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    return controller.delete_product(product_id)