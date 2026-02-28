


import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "productsdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    return psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    company_name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    active BOOLEAN DEFAULT TRUE
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    category_id SERIAL PRIMARY KEY,
                    category_name VARCHAR(255) NOT NULL UNIQUE,
                    active BOOLEAN DEFAULT TRUE
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    company_id UUID NOT NULL REFERENCES companies(company_id) ON DELETE CASCADE,
                    company_name VARCHAR(255) NOT NULL,
                    description TEXT,
                    price NUMERIC(10,2),
                    active BOOLEAN DEFAULT TRUE
);
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS warranties (
                    warranty_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    product_id UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
                    warranty_months INTEGER NOT NULL
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS productscategoriesxref (
                    product_id UUID NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
                    category_id INTEGER NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
                    PRIMARY KEY (product_id, category_id)
                );
                """
            )

        conn.commit()


        