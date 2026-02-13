from flask import jsonify, request
from db import get_connection


def add_category():
    post_data = request.form if request.form else request.json

    if "category_name" not in post_data:
        return jsonify({"message": "category_name is required"}), 400

    category_name = post_data["category_name"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO categories (category_name)
                VALUES (%s)
                RETURNING category_id, category_name;
            """, (category_name,))
            row = cur.fetchone()

    category = {
        "category_id": str(row[0]),
        "category_name": row[1]
    }

    return jsonify({"message": "category added", "result": category}), 201


def get_category_by_id(category_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT category_id, category_name
                FROM categories
                WHERE category_id = %s;
            """, (category_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "category not found"}), 400

    category = {
        "category_id": str(row[0]),
        "category_name": row[1]
    }

    return jsonify({"message": "category found", "result": category}), 200


def get_all_categories():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT category_id, category_name
                FROM categories;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "category_id": str(row[0]),
            "category_name": row[1]
        })

    return jsonify({"message": "categories found", "results": results}), 200


def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT category_id, category_name
                FROM categories
                WHERE category_id = %s;
            """, (category_id,))
            row = cur.fetchone()

            if not row:
                return jsonify({"message": "category not found"}), 400

            category_name = post_data.get("category_name", row[1])

            cur.execute("""
                UPDATE categories
                SET category_name = %s
                WHERE category_id = %s
                RETURNING category_id, category_name;
            """, (category_name, category_id))
            updated = cur.fetchone()

    category = {
        "category_id": str(updated[0]),
        "category_name": updated[1]
    }

    return jsonify({"message": "category updated", "result": category}), 200


def delete_category(category_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM categories
                WHERE category_id = %s
                RETURNING category_id;
            """, (category_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "category not found"}), 400

    return jsonify({"message": "category delete"}), 200