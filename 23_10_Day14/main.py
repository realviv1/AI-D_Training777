from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def home():
    return {"message": "Product Store API is running"}

@app.get("/products")
def get_products():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id, name, price, image FROM products"
        )
        rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            }
            for row in rows
        ]
    finally:
        cur.close()
        conn.close()


