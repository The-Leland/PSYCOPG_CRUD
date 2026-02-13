from flask import Blueprint
from controllers import category_controller as controller

category = Blueprint('category', __name__)

@category.route('/category', methods=['POST'])
def add_category_route():
    return controller.add_category()

@category.route('/category/<category_id>', methods=['GET'])
def get_category_by_id_route(category_id):
    return controller.get_category_by_id(category_id)

@category.route('/categories', methods=['GET'])
def get_all_categories_route():
    return controller.get_all_categories()

@category.route('/category/<category_id>', methods=['PUT'])
def update_category_by_id_route(category_id):
    return controller.update_category_by_id(category_id)

@category.route('/category/<category_id>', methods=['DELETE'])
def delete_category_route(category_id):
    return controller.delete_category(category_id)