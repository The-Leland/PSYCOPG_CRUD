


from flask import jsonify, request

from db import get_connection


def add_product():
    post_data = request.form if request.form else request.json

    if "company_id" not in post_data or "company_name" not in post_data:
        return jsonify({"message": "company_id and company_name are required"}), 400

    active_value = post_data.get("active", True)

    company_id = post_data["company_id"]
    company_name = post_data["company_name"]
    description = post_data.get("description")
    price = post_data.get("price")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (company_id, company_name, description, price, active)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING product_id, company_id, company_name, description, price, active;
            """, (company_id, company_name, description, price, active_value))

            row = cur.fetchone()

    product = {
        "product_id": str(row[0]),
        "company_id": str(row[1]),
        "company_name": row[2],
        "description": row[3],
        "price": row[4],
        "active": row[5]
    }

    return jsonify({"message": "product added", "result": product}), 201


def get_product_by_id(product_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, company_id, company_name, description, price, active
                FROM products
                WHERE product_id = %s;
            """, (product_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "product not found"}), 400

    product = {
        "product_id": str(row[0]),
        "company_id": str(row[1]),
        "company_name": row[2],
        "description": row[3],
        "price": row[4],
        "active": row[5]
    }

    return jsonify({"message": "product found", "result": product}), 200


def get_all_products():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, company_id, company_name, description, price, active
                FROM products;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "product_id": str(row[0]),
            "company_id": str(row[1]),
            "company_name": row[2],
            "description": row[3],
            "price": row[4],
            "active": row[5]
        })

    return jsonify({"message": "products found", "results": results}), 200


def get_active_products():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, company_id, company_name, description, price, active
                FROM products
                WHERE active = TRUE;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "product_id": str(row[0]),
            "company_id": str(row[1]),
            "company_name": row[2],
            "description": row[3],
            "price": row[4],
            "active": row[5]
        })

    return jsonify({"message": "active products", "results": results}), 200


def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, company_id, company_name, description, price, active
                FROM products
                WHERE product_id = %s;
            """, (product_id,))
            row = cur.fetchone()

            if not row:
                return jsonify({"message": "product not found"}), 400

            company_id = post_data.get("company_id", row[1])
            company_name = post_data.get("company_name", row[2])
            description = post_data.get("description", row[3])
            price = post_data.get("price", row[4])
            active = post_data.get("active", row[5])

            cur.execute("""
                UPDATE products
                SET company_id = %s,
                    company_name = %s,
                    description = %s,
                    price = %s,
                    active = %s
                WHERE product_id = %s
                RETURNING product_id, company_id, company_name, description, price, active;
            """, (company_id, company_name, description, price, active, product_id))

            updated = cur.fetchone()

    product = {
        "product_id": str(updated[0]),
        "company_id": str(updated[1]),
        "company_name": updated[2],
        "description": updated[3],
        "price": updated[4],
        "active": updated[5]
    }

    return jsonify({"message": "product updated", "result": product}), 200


def update_product_active(product_id):
    post_data = request.form if request.form else request.json

    if "active" not in post_data:
        return jsonify({"message": "active field required"}), 400

    active_value = post_data["active"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE products
                SET active = %s
                WHERE product_id = %s
                RETURNING product_id, company_id, company_name, description, price, active;
            """, (active_value, product_id))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "product not found"}), 400

    product = {
        "product_id": str(row[0]),
        "company_id": str(row[1]),
        "company_name": row[2],
        "description": row[3],
        "price": row[4],
        "active": row[5]
    }

    return jsonify({"message": "active updated", "result": product}), 200


def delete_product(product_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM products
                WHERE product_id = %s
                RETURNING product_id;
            """, (product_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "product not found"}), 400

    return jsonify({"message": "product delete"}), 200