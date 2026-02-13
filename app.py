from flask import Flask
from routes.product_routes import product
from routes.company_routes import company
from routes.category_routes import category
from routes.warranty_routes import warranty
from routes.xref_routes import xref

app = Flask(__name__)

app.register_blueprint(product)
app.register_blueprint(company)
app.register_blueprint(category)
app.register_blueprint(warranty)
app.register_blueprint(xref)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)