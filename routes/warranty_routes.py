from flask import Blueprint
from db import get_connection

from controllers import warranty_controller as controller

warranty = Blueprint('warranty', __name__)

@warranty.route('/warranty', methods=['POST'])
def add_warranty_route():
    return controller.add_warranty()

@warranty.route('/warranty/<warranty_id>', methods=['GET'])
def get_warranty_by_id_route(warranty_id):
    return controller.get_warranty_by_id(warranty_id)

@warranty.route('/warranties', methods=['GET'])
def get_all_warranties_route():
    return controller.get_all_warranties()

@warranty.route('/warranty/<warranty_id>', methods=['PUT'])
def update_warranty_by_id_route(warranty_id):
    return controller.update_warranty_by_id(warranty_id)

@warranty.route('/warranty/<warranty_id>', methods=['DELETE'])
def delete_warranty_route(warranty_id):
    return controller.delete_warranty(warranty_id)

