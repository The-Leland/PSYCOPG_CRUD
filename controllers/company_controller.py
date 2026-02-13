


from flask import jsonify, request
from db import get_connection


def add_company():
    post_data = request.form if request.form else request.json

    if "company_name" not in post_data:
        return jsonify({"message": "company_name is required"}), 400

    company_name = post_data["company_name"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO companies (company_name)
                VALUES (%s)
                RETURNING company_id, company_name;
            """, (company_name,))
            row = cur.fetchone()

    company = {
        "company_id": str(row[0]),
        "company_name": row[1]
    }

    return jsonify({"message": "company added", "result": company}), 201


def get_company_by_id(company_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_id, company_name
                FROM companies
                WHERE company_id = %s;
            """, (company_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "company not found"}), 400

    company = {
        "company_id": str(row[0]),
        "company_name": row[1]
    }

    return jsonify({"message": "company found", "result": company}), 200


def get_all_companies():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_id, company_name
                FROM companies;
            """)
            rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "company_id": str(row[0]),
            "company_name": row[1]
        })

    return jsonify({"message": "companies found", "results": results}), 200


def update_company_by_id(company_id):
    post_data = request.form if request.form else request.json

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_id, company_name
                FROM companies
                WHERE company_id = %s;
            """, (company_id,))
            row = cur.fetchone()

            if not row:
                return jsonify({"message": "company not found"}), 400

            company_name = post_data.get("company_name", row[1])

            cur.execute("""
                UPDATE companies
                SET company_name = %s
                WHERE company_id = %s
                RETURNING company_id, company_name;
            """, (company_name, company_id))
            updated = cur.fetchone()

    company = {
        "company_id": str(updated[0]),
        "company_name": updated[1]
    }

    return jsonify({"message": "company updated", "result": company}), 200


def delete_company(company_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM companies
                WHERE company_id = %s
                RETURNING company_id;
            """, (company_id,))
            row = cur.fetchone()

    if not row:
        return jsonify({"message": "company not found"}), 400

    return jsonify({"message": "company delete"}), 200