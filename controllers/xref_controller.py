from flask import jsonify, request
from db import get_connection


def add_xref():
    post_data = request.form if request.form else request.json

    if "product_id" not in post_data or "category_id" not in post_data:
        return jsonify({"message": "product_id and category_id are required"}), 400

    product_id = post_data["product_id"]
    category_id = post_data["category_id"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO productscategoriesxref (product_id, category_id)
                VALUES (%s, %s)
                RETURNING product_id, category_id;
            """, (product_id, category_id))
            row = cur.fetchone()

    xref = {
        "product_id": str(row[0]),
        "category_id": str(row[1])
    }

    return jsonify({"message": "xref added", "result": xref}), 201


def get_xref_by_ids(product_id, category_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, category_id
                FROM productscategoriesxref
                WHERE product_id = %s AND category_id = %s;
            """, (product_id, category_id))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "xref not found"}), 400

    xref = {
        "product_id": str(row[0]),
        "category_id": str(row[1])
    }

    return jsonify({"message": "xref found", "result": xref}), 200


def get_all_xrefs():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT product_id, category_id
                FROM productscategoriesxref;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "product_id": str(row[0]),
            "category_id": str(row[1])
        })

    return jsonify({"message": "xrefs found", "results": results}), 200


def delete_xref(product_id, category_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM productscategoriesxref
                WHERE product_id = %s AND category_id = %s
                RETURNING product_id;
            """, (product_id, category_id))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "xref not found"}), 400

    return jsonify({"message": "xref delete"}), 200