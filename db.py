


# product_records = [
#     {
#         "product_id": "1",
#         "product_name": "Hasbro Gaming Clue Game",
#         "description": "One murder... 6 suspects...",
#         "price": 9.95,
#         "active": True
#     },
#     {
#         "product_id": "2",
#         "product_name": "Monopoly Board Game The Classic Edition, 2-8 players",
#         "description": "Relive the Monopoly experiences...",
#         "price": 35.50,
#         "active": True
#     }
# ]



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
            # Enable UUID generation
            cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    company_name VARCHAR NOT NULL UNIQUE
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    category_name VARCHAR NOT NULL UNIQUE
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    company_id UUID REFERENCES companies(company_id),
                    company_name VARCHAR NOT NULL UNIQUE,
                    price INTEGER,
                    description VARCHAR,
                    active BOOLEAN DEFAULT TRUE
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS productscategoriesxref (
                    product_id UUID REFERENCES products(product_id),
                    category_id UUID REFERENCES categories(category_id),
                    PRIMARY KEY (product_id, category_id)
                );
                """
            )

        conn.commit()