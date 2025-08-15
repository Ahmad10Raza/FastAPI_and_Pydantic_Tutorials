
### 1. **Validation**

FastAPI automatically validates incoming data against the schema you define with  **Pydantic models** .

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, constr

app = FastAPI()

class User(BaseModel):
    username: constr(min_length=3, max_length=20)  # must be 3–20 chars
    email: EmailStr                               # must be a valid email
    age: int

@app.post("/users/")
async def create_user(user: User):
    return {"msg": "User created", "data": user}
```

* If a client sends `{"username": "ab", "email": "not-an-email", "age": "twenty"}`,

  FastAPI will **auto-return a 422 error** with details about what failed.

---

### 2. **Aliases**

Sometimes request/response fields differ from Python variable names.

You can use **aliases** to map JSON fields to Python attributes.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., alias="user_name")   # expect `user_name` in JSON
    age: int

@app.post("/users/")
async def create_user(user: User):
    return {"username": user.username, "age": user.age}
```

* Incoming request:
  ```json
  { "user_name": "Ahmad", "age": 22 }
  ```
* FastAPI converts `"user_name"` → `username` internally.

---

### 3. **Nested Models**

You can embed one Pydantic model inside another. This allows  **hierarchical data validation** .

```python
from typing import List

class Address(BaseModel):
    city: str
    zipcode: str

class User(BaseModel):
    username: str
    email: EmailStr
    addresses: List[Address]   # list of nested models

@app.post("/users/")
async def create_user(user: User):
    return user
```

* Example request:
  ```json
  {
    "username": "ahmad",
    "email": "ahmad@example.com",
    "addresses": [
      {"city": "Delhi", "zipcode": "110001"},
      {"city": "Mumbai", "zipcode": "400001"}
    ]
  }
  ```

✅ FastAPI ensures:

* `email` is valid.
* `addresses` is a list.
* Each item matches `Address` model schema.

---

🔑 **Why this matters:**

* You **define contracts once** with Pydantic.
* FastAPI automatically validates input/output.
* Errors are clear and structured, no need to write extra validation code.

---


In  **FastAPI** , you can combine  **request body** ,  **query parameters** , and **path parameters** in a single endpoint. This makes APIs more expressive and flexible. Let’s break it down:

---

### 1. Path Parameters + Request Body

Path params identify resources. The body carries structured data.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/users/{user_id}/items/")
async def create_item(user_id: int, item: Item):
    return {
        "user_id": user_id,
        "item": item.dict()
    }
```

* `user_id`: from **path** (`/users/10/items/`)
* `item`: from **body** (`{"name": "Laptop", "price": 1200}`)

---

### 2. Query Parameters + Request Body

Queries are useful for filters or optional modifiers.

```python
@app.post("/items/")
async def create_item(item: Item, discount: float = 0.0, in_stock: bool = True):
    final_price = item.price - discount
    return {
        "item": item.dict(),
        "discount": discount,
        "in_stock": in_stock,
        "final_price": final_price
    }
```

Example request:

```
POST /items/?discount=100&in_stock=false
Body: {"name": "Phone", "price": 500}
```

---

### 3. Path + Query + Body Together

You can combine all three in one endpoint.

```python
@app.put("/users/{user_id}/items/{item_id}")
async def update_item(
    user_id: int,
    item_id: int,
    item: Item,
    notify: bool = False
):
    return {
        "user_id": user_id,        # from path
        "item_id": item_id,        # from path
        "notify": notify,          # from query (?notify=true)
        "updated_item": item.dict()  # from body
    }
```

Request example:

```
PUT /users/5/items/99?notify=true
Body: {"name": "Tablet", "price": 750}
```

Response:

```json
{
  "user_id": 5,
  "item_id": 99,
  "notify": true,
  "updated_item": {"name": "Tablet", "price": 750}
}
```

---

✅ **Key Points**

* Path params = part of URL (required).
* Query params = optional filters/modifiers in URL.
* Body = structured data (JSON, form, etc.).
* FastAPI automatically validates and merges them into function parameters.

---

In FastAPI, request bodies and query/path parameters can include  **lists, dictionaries, and optional fields** . These allow you to model real-world data more flexibly. FastAPI leverages **Pydantic** to handle parsing and validation automatically.

---

### 1. **Handling Lists**

* Lists are useful for multiple values (tags, IDs, etc.).
* FastAPI automatically parses query params and JSON arrays into Python `list`.

#### Example: Query parameter as list

```python
from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/items/")
async def get_items(tags: List[str] = []):
    return {"tags": tags}
```

**Request:**

```
GET /items/?tags=python&tags=fastapi&tags=ai
```

**Response:**

```json
{"tags": ["python", "fastapi", "ai"]}
```

#### Example: Request body list

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_items(items: List[Item]):
    return {"items": items}
```

**Request body:**

```json
[
  {"name": "Book", "price": 12.5},
  {"name": "Pen", "price": 2.0}
]
```

---

### 2. **Handling Dictionaries**

* Useful when keys are dynamic.
* FastAPI automatically parses JSON objects into Python `dict`.

#### Example: Dictionary request body

```python
from typing import Dict

@app.post("/attributes/")
async def create_attributes(attributes: Dict[str, str]):
    return {"attributes": attributes}
```

**Request body:**

```json
{"color": "red", "size": "M", "brand": "Nike"}
```

**Response:**

```json
{"attributes": {"color": "red", "size": "M", "brand": "Nike"}}
```

---

### 3. **Optional Fields**

* Sometimes values may not be present.
* Use `Optional` from `typing` or assign a default.

#### Example: Optional field in model

```python
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None  # optional

@app.post("/users/")
async def create_user(user: User):
    return user
```

**Request body:**

```json
{"id": 1, "name": "Alice"}
```

**Response:**

```json
{"id": 1, "name": "Alice", "email": null}
```

---

✅ **Key points**

* `List[]`: handles arrays (query/body).
* `Dict[]`: handles objects with dynamic keys.
* `Optional[]` or `= None`: allows missing/nullable fields.

---

In FastAPI, error handling is a structured way to control what happens when things go wrong in your API. Instead of letting your app crash or return generic errors, you can send proper HTTP error responses with useful information.

---

### 1. Using `HTTPException`

FastAPI provides `HTTPException` to raise standard HTTP errors.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {1: "Alice", 2: "Bob"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    return {"user_id": user_id, "name": users[user_id]}
```

* `status_code`: the HTTP status code (e.g., 404, 403, 400).
* `detail`: extra information for the client.
* FastAPI automatically converts it into a JSON response.

Response example:

```json
{
  "detail": "User with ID 3 not found"
}
```

---

### 2. Custom error handlers

Sometimes you want to catch specific exceptions and return custom responses.

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(DatabaseConnectionError)
async def db_error_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=500,
        content={"error": "Database error", "message": exc.message}
    )

@app.get("/db-test")
def test_db():
    raise DatabaseConnectionError("Unable to connect to DB")
```

Now, instead of a raw traceback, the client gets:

```json
{
  "error": "Database error",
  "message": "Unable to connect to DB"
}
```

---

### 3. Built-in exception handlers

FastAPI already has handlers for some common exceptions:

* `RequestValidationError` → Raised when request data doesn’t match Pydantic model.
* `HTTPException` → As shown above.

You can override them if needed:

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid input", "details": exc.errors()}
    )
```

---

### 4. Return custom response codes

Instead of raising an exception, you can manually return errors:

```python
from fastapi.responses import JSONResponse

@app.get("/check/{num}")
def check_number(num: int):
    if num < 0:
        return JSONResponse(status_code=400, content={"error": "Negative numbers not allowed"})
    return {"num": num}
```

---

✅ Summary of Error Handling in FastAPI:

* Use `HTTPException` for simple HTTP errors.
* Use `@app.exception_handler` for custom exceptions.
* Override built-in handlers (`RequestValidationError`, etc.) for better error formatting.
* Use custom responses (`JSONResponse`) if you want full control.
