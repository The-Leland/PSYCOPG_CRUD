from flask import jsonify, request
from db import get_connection


def add_warranty():
    post_data = request.form if request.form else request.json

    if "product_id" not in post_data or "warranty_months" not in post_data:
        return jsonify({"message": "product_id and warranty_months are required"}), 400

    product_id = post_data["product_id"]
    warranty_months = post_data["warranty_months"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO warranties (product_id, warranty_months)
                VALUES (%s, %s)
                RETURNING warranty_id, product_id, warranty_months;
            """, (product_id, warranty_months))
            row = cur.fetchone()

    warranty = {
        "warranty_id": str(row[0]),
        "product_id": str(row[1]),
        "warranty_months": row[2]
    }

    return jsonify({"message": "warranty added", "result": warranty}), 201


def get_warranty_by_id(warranty_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT warranty_id, product_id, warranty_months
                FROM warranties
                WHERE warranty_id = %s;
            """, (warranty_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "warranty not found"}), 400

    warranty = {
        "warranty_id": str(row[0]),
        "product_id": str(row[1]),
        "warranty_months": row[2]
    }

    return jsonify({"message": "warranty found", "result": warranty}), 200


def get_all_warranties():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT warranty_id, product_id, warranty_months
                FROM warranties;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "warranty_id": str(row[0]),
            "product_id": str(row[1]),
            "warranty_months": row[2]
        })

    return jsonify({"message": "warranties found", "results": results}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT warranty_id, product_id, warranty_months
                FROM warranties
                WHERE warranty_id = %s;
            """, (warranty_id,))
            row = cur.fetchone()

            if not row:
                return jsonify({"message": "warranty not found"}), 400

            product_id = post_data.get("product_id", row[1])
            warranty_months = post_data.get("warranty_months", row[2])

            cur.execute("""
                UPDATE warranties
                SET product_id = %s,
                    warranty_months = %s
                WHERE warranty_id = %s
                RETURNING warranty_id, product_id, warranty_months;
            """, (product_id, warranty_months, warranty_id))
            updated = cur.fetchone()

    warranty = {
        "warranty_id": str(updated[0]),
        "product_id": str(updated[1]),
        "warranty_months": updated[2]
    }

    return jsonify({"message": "warranty updated", "result": warranty}), 200


def delete_warranty(warranty_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM warranties
                WHERE warranty_id = %s
                RETURNING warranty_id;
            """, (warranty_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "warranty not found"}), 400

    return jsonify({"message": "warranty delete"}), 200
