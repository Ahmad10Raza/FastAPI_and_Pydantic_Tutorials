
---

### 1. The FastAPI App

Every FastAPI project starts with an  **app instance** :

```python
from fastapi import FastAPI

app = FastAPI()
```

This `app` is your main web application object. You define **routes (endpoints)** on it using decorators like `@app.get`, `@app.post`, etc.

---

### 2. The `@app.get("/")` Route

* **`@app.get("/")`** means:

  "When someone makes a `GET` request to the `/` path, run this function."

Example:

```python
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with GET!"}
```

* If you visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/), you’ll see:

```json
{"message": "Hello, FastAPI with GET!"}
```

---

### 3. The `@app.post("/")` Route

* **`@app.post("/")`** means:

  "When someone makes a `POST` request to the `/` path, run this function."

Example:

```python
@app.post("/")
def create_item():
    return {"message": "You made a POST request!"}
```

* If you send a **POST request** to `/` (using Postman, curl, or Swagger UI), you’ll get:

```json
{"message": "You made a POST request!"}
```

---

### 4. Why Different Methods?

HTTP methods define  **the action** :

* `GET` → Retrieve data (read-only, safe to repeat).
* `POST` → Send data (create something new on the server).
* `PUT` → Update existing data.
* `DELETE` → Remove data.

FastAPI lets you map these methods directly with decorators.

---

### 5. Example with Both Together

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"method": "GET", "message": "Hello from GET!"}

@app.post("/")
def create_root():
    return {"method": "POST", "message": "Hello from POST!"}
```

* If you visit `/` in your browser → you trigger `GET` (you’ll see `"Hello from GET!"`).
* If you send a `POST` request (via Swagger UI or Postman) → you’ll see `"Hello from POST!"`.



---

### **1. `@app.get()`**

* **Purpose** : Retrieve data (read-only operation).
* **Safe** : Does not modify server state.
* **Idempotent** : Calling it multiple times gives the same result.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items():
    return {"message": "List of items"}
```

Example request:

```
GET /items
```

---

### **2. `@app.post()`**

* **Purpose** : Create new data or perform actions that change the server state.
* **Not idempotent** : Multiple calls may create multiple entries.

```python
@app.post("/items")
def create_item(item: dict):
    return {"message": "Item created", "data": item}
```

Example request:

```
POST /items
Body: {"name": "Book", "price": 100}
```

---

### **3. `@app.put()`**

* **Purpose** : Update or replace an existing resource  **entirely** .
* **Idempotent** : Multiple identical calls give the same result.

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"message": f"Item {item_id} updated", "data": item}
```

Example request:

```
PUT /items/1
Body: {"name": "Updated Book", "price": 120}
```

---

### **4. `@app.delete()`**

* **Purpose** : Delete a resource.
* **Idempotent** : Deleting the same resource multiple times has the same result (gone).

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

Example request:

```
DELETE /items/1
```

---

### **Summary of HTTP Methods in FastAPI**

| Decorator         | Method | Purpose                           | Idempotent | Safe   |
| ----------------- | ------ | --------------------------------- | ---------- | ------ |
| `@app.get()`    | GET    | Fetch data                        | ✅ Yes     | ✅ Yes |
| `@app.post()`   | POST   | Create new data / trigger actions | ❌ No      | ❌ No  |
| `@app.put()`    | PUT    | Update/replace existing resource  | ✅ Yes     | ❌ No  |
| `@app.delete()` | DELETE | Remove resource                   | ✅ Yes     | ❌ No  |


---

### 1. Dynamic Routes

FastAPI allows **dynamic paths** using curly braces `{}` inside the route definition.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

* `/users/101` → `{"user_id": 101}`
* `/users/abc` → validation error (since `user_id` is declared as `int`).

Here, `{user_id}` is a  **path parameter** .

FastAPI automatically parses it from the URL and injects it into the function.

---

### 2. Type Validation for Path Params

FastAPI uses **Python type hints** to validate path parameters.

Example:

```python
@app.get("/items/{item_id}")
def get_item(item_id: str, quantity: int):
    return {"item_id": item_id, "quantity": quantity}
```

* `http://127.0.0.1:8000/items/book?quantity=5` → ✅ Works
* If you pass `quantity=abc` → ❌ Validation error (expects `int`).

---

### 3. Multiple Path Parameters

```python
@app.get("/orders/{order_id}/items/{item_id}")
def get_order_item(order_id: int, item_id: str):
    return {"order_id": order_id, "item_id": item_id}
```

URL: `/orders/10/items/pen` → `{"order_id": 10, "item_id": "pen"}`

---

### 4. Adding Metadata and Validation

You can add constraints using `Path` from `fastapi`.

```python
from fastapi import Path

@app.get("/products/{product_id}")
def read_product(
    product_id: int = Path(..., title="The ID of the product", ge=1, le=1000)
):
    return {"product_id": product_id}
```

* `ge=1` → product_id must be ≥ 1
* `le=1000` → product_id must be ≤ 1000
* If user passes `/products/0` → error: value not allowed.

---

### 5. Optional Path Parameters

All path parameters are  **required by default** , unlike query parameters.

You cannot make them optional, but you can make them accept `str` with default value via query parameter instead.


---

### 1. What Are Query Parameters?

Query parameters are the part of the URL that comes  **after the `?` symbol** .

They are **not** part of the path, but are added in key-value pairs.

Example URL:

```
http://127.0.0.1:8000/items/?category=books&limit=10
```

Here:

* `category=books`
* `limit=10`

---

### 2. Using Query Parameters in FastAPI

You define them as function arguments  **that are not in the path** .

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(category: str, limit: int):
    return {"category": category, "limit": limit}
```

Request:

```
GET /items/?category=books&limit=10
```

Response:

```json
{"category": "books", "limit": 10}
```

---

### 3. Optional Query Parameters

If you want a query parameter to be  **optional** , use `Optional` or give it a default value.

```python
from typing import Optional

@app.get("/products/")
def read_products(category: Optional[str] = None):
    if category:
        return {"message": f"Filtering products in {category}"}
    return {"message": "Showing all products"}
```

* `/products/` → `{"message": "Showing all products"}`
* `/products/?category=shoes` → `{"message": "Filtering products in shoes"}`

---

### 4. Default Values for Query Parameters

You can assign a default value to query parameters.

```python
@app.get("/search/")
def search_items(q: str = "all", limit: int = 10):
    return {"query": q, "limit": limit}
```

* `/search/` → `{"query": "all", "limit": 10}`
* `/search/?q=laptop` → `{"query": "laptop", "limit": 10}`
* `/search/?q=phone&limit=5` → `{"query": "phone", "limit": 5}`

---

### 5. Combining Path and Query Parameters

You can use both together.

```python
@app.get("/users/{user_id}/orders/")
def get_orders(user_id: int, status: Optional[str] = None):
    return {"user_id": user_id, "status": status}
```

* `/users/10/orders/` → `{"user_id": 10, "status": null}`
* `/users/10/orders/?status=pending` → `{"user_id": 10, "status": "pending"}`
