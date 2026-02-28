


from flask import Blueprint
from controllers import xref_controller as controller

xref = Blueprint('xref', __name__)

@xref.route('/product/category', methods=['POST'])
def add_xref_route():
    return controller.add_xref()

@xref.route('/product/category/<product_id>/<category_id>', methods=['GET'])
def get_xref_by_ids_route(product_id, category_id):
    return controller.get_xref_by_ids(product_id, category_id)

@xref.route('/product/categories', methods=['GET'])
def get_all_xrefs_route():
    return controller.get_all_xrefs()

@xref.route('/product/category/<product_id>/<category_id>', methods=['DELETE'])
def delete_xref_route(product_id, category_id):
    return controller.delete_xref(product_id, category_id)


