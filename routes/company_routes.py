



from flask import Blueprint
from db import get_connection


from controllers import company_controller as controller

company = Blueprint('company', __name__)

@company.route('/company', methods=['POST'])
def add_company_route():
    return controller.add_company()

@company.route('/company/<company_id>', methods=['GET'])
def get_company_by_id_route(company_id):
    return controller.get_company_by_id(company_id)

@company.route('/companies', methods=['GET'])
def get_all_companies_route():
    return controller.get_all_companies()

@company.route('/company/<company_id>', methods=['PUT'])
def update_company_by_id_route(company_id):
    return controller.update_company_by_id(company_id)

@company.route('/company/<company_id>', methods=['DELETE'])
def delete_company_route(company_id):
    return controller.delete_company(company_id)