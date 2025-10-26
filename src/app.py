from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List
from fastapi.responses import JSONResponse

app = FastAPI(title="Product CRUD API", version="1.0.0")


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class Product(ProductCreate):
    id: int


# In-memory store
_products: Dict[int, Product] = {}
_next_id: int = 1


def _generate_id() -> int:
    global _next_id
    new_id = _next_id
    _next_id += 1
    return new_id


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/products", status_code=201, response_model=Product)
def create_product(payload: ProductCreate):
    new_id = _generate_id()
    product = Product(id=new_id, **payload.dict())
    _products[new_id] = product
    return product


@app.get("/products", response_model=List[Product])
def list_products():
    return list(_products.values())


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = _products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, payload: ProductCreate):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = Product(id=product_id, **payload.dict())
    _products[product_id] = updated
    return updated


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    del _products[product_id]
    return JSONResponse(status_code=204, content=None)
