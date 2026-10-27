from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float
    image: str

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="product_store",
        user="postgres",
        password="Admin@123"
    )

@app.get("/products")
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,name,price,image
        FROM products
        ORDER BY id
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "image": row[3]
        })

    return products

@app.post("/products")
def add_product(product: Product):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO products(id,name,price,image)
        VALUES(%s,%s,%s,%s)
        """,
        (
            product.id,
            product.name,
            product.price,
            product.image
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product Added"}

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name=%s,
            price=%s,
            image=%s
        WHERE id=%s
        """,
        (
            product.name,
            product.price,
            product.image,
            product_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product Updated"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (product_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Product Deleted"}