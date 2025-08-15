In FastAPI, handling request and response data is one of the most powerful features because it leverages **Pydantic models** for validation, parsing, and serialization.

### **Request Body Parsing with Pydantic Models**

#### 1. Why use Pydantic models for request bodies?

* They automatically:
  * Validate incoming JSON data against your schema.
  * Convert types (e.g., `"25"` → `int`).
  * Provide clear error messages if validation fails.
* Ensures that your API always works with  **clean and predictable data** .

---

#### 2. Defining a request model

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define schema for request body
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True   # default value

# Endpoint accepting request body
@app.post("/users/")
async def create_user(user: User):
    return {"message": "User created successfully", "user": user}
```

##### Example Request:

```json
POST /users/
{
  "id": 1,
  "name": "Ahmad",
  "email": "ahmad@example.com"
}
```

##### Example Response:

```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "name": "Ahmad",
    "email": "ahmad@example.com",
    "is_active": true
  }
}
```

---

#### 3. Multiple request bodies

You can accept more than one model in a request:

```python
class Address(BaseModel):
    city: str
    zipcode: str

@app.post("/register/")
async def register(user: User, address: Address):
    return {"user": user, "address": address}
```

Request JSON must contain **both `user` and `address`** objects.

---

#### 4. Nested models

Models can contain other models:

```python
class Address(BaseModel):
    city: str
    zipcode: str

class User(BaseModel):
    id: int
    name: str
    address: Address

@app.post("/nested/")
async def create_nested(user: User):
    return user
```

Request:

```json
{
  "id": 1,
  "name": "Ahmad",
  "address": {
    "city": "Lucknow",
    "zipcode": "226001"
  }
}
```

---

#### 5. Request body + path/query params

You can combine them:

```python
@app.post("/items/{item_id}")
async def update_item(item_id: int, user: User, q: str = None):
    return {"item_id": item_id, "q": q, "user": user}
```

Request URL:

```
POST /items/42?q=test
```

Body:

```json
{
  "id": 101,
  "name": "Ahmad",
  "email": "ahmad@example.com"
}
```

---

✅ **Key Point:**

FastAPI uses **Pydantic models** for request bodies so you always get structured, validated, and type-safe input.


---



In FastAPI, handling **form data** and **file uploads** is straightforward. FastAPI provides special classes like `Form`, `File`, and `UploadFile` to deal with these cases.

---

### 1. **Form Data (`Form`)**

* Used when clients submit form data (like HTML forms with `application/x-www-form-urlencoded` or `multipart/form-data`).
* Instead of JSON, the data comes as  **key-value pairs** .

#### Example: Handling login form

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "message": "Login successful"}
```

* `Form(...)` makes the field  **required** .
* Clients can send data like:
  ```bash
  curl -X POST "http://127.0.0.1:8000/login/" -d "username=ahmad&password=1234"
  ```

---

### 2. **File Uploads**

FastAPI has two main ways to handle file uploads:

* `File`: Reads file content into  **bytes** .
* `UploadFile`: A more efficient option with **streaming** and extra methods.

#### a) Using `File` (simple, small files)

```python
from fastapi import FastAPI, File

app = FastAPI()

@app.post("/upload-file/")
async def upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}
```

* Here, the entire file is read into memory as `bytes`.
* Good for small files like text or images.

---

#### b) Using `UploadFile` (recommended)

```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }
```

* `UploadFile` gives you:
  * `.filename` → Original filename
  * `.content_type` → MIME type
  * `.file` → A Python file-like object you can read/write/stream
* Efficient for **large files** since it doesn’t load the entire file into memory.

---

### 3. **Uploading Multiple Files**

```python
from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/upload-multiple/")
async def upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}
```

* Accepts multiple files at once.
* Clients can send:
  ```bash
  curl -X POST "http://127.0.0.1:8000/upload-multiple/" \
       -F "files=@file1.txt" \
       -F "files=@file2.jpg"
  ```

---

✅ **Summary**

* `Form(...)`: Use for form fields like text input, passwords, etc.
* `File(...)`: Reads file directly into memory as bytes (good for small files).
* `UploadFile(...)`: Streams file, more efficient for large uploads, has metadata.

---


In  **FastAPI** , a `response_model` is used to define the shape (schema) of the data returned by your API endpoint. It helps you enforce a  **consistent response structure** , validate outgoing responses, and generate **clear API documentation** automatically.

---

### Why use `response_model`?

* Ensures **data validation** before sending the response.
* Prevents **leaking sensitive fields** (like passwords).
* Automatically adds to  **OpenAPI docs** .
* Can **transform data** (e.g., hiding internal fields, renaming).

---

### Basic Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request model
class UserIn(BaseModel):
    username: str
    password: str

# Response model (hides password)
class UserOut(BaseModel):
    username: str

@app.post("/user/", response_model=UserOut)
def create_user(user: UserIn):
    # Normally, you'd save the user in DB here
    return user   # Only `username` will be returned (password excluded)
```

**Output Example**

```json
# Request
{
  "username": "ahmad",
  "password": "secret123"
}

# Response
{
  "username": "ahmad"
}
```

Notice how `password` was **excluded** because of `response_model=UserOut`.

---

### With Lists

```python
@app.get("/users/", response_model=list[UserOut])
def get_users():
    return [
        {"username": "alice", "password": "hidden"},
        {"username": "bob", "password": "hidden"}
    ]
```

Response will only return usernames.

---

### Advanced Features

* **`response_model_exclude_unset=True`** → removes unset (default) fields.
* **`response_model_include={"username"}`** → include only specific fields.
* **`response_model_exclude={"password"}`** → exclude sensitive fields.

```python
@app.post("/user/full/", response_model=UserOut, response_model_exclude={"password"})
def create_user_with_exclusion(user: UserIn):
    return user
```

---

✅ In short:

`response_model` is like a **filter and validator** for your API responses. It ensures clients receive exactly what you want them to see.



In  **FastAPI** , the `status_code` parameter is used in route decorators (like `@app.get`, `@app.post`, etc.) to define the **default HTTP status code** that your endpoint should return.

---

### Why use `status_code`?

* Makes API responses **more meaningful** (e.g., 201 for created resources, 404 for not found).
* Ensures your API follows  **REST best practices** .
* Automatically appears in the  **OpenAPI documentation** .

---

### Example: `status_code=201`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/", status_code=201)
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

**Request**

```json
{
  "name": "Laptop",
  "price": 75000
}
```

**Response**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "name": "Laptop",
  "price": 75000
}
```

---

### Commonly used status codes

* `200 OK` → default for most successful responses.
* `201 Created` → when a new resource is created (e.g., POST).
* `202 Accepted` → request accepted but still processing.
* `204 No Content` → success but no response body.
* `400 Bad Request` → client sent invalid data.
* `401 Unauthorized` → authentication required.
* `403 Forbidden` → client doesn’t have permission.
* `404 Not Found` → resource doesn’t exist.
* `500 Internal Server Error` → unexpected server error.

---

### Example with `status_code=204`

```python
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    # delete item logic
    return None   # No response body, just 204 status
```

**Response**

```http
HTTP/1.1 204 No Content
```

---

✅ So `status_code=201` tells FastAPI (and clients) that a new resource has been created successfully.



In  **FastAPI** , by default, responses are returned as JSON, but you can **customize the response type** using classes like `JSONResponse`, `HTMLResponse`, or `RedirectResponse`. These are part of  **Starlette** , the underlying framework FastAPI is built on.

---

## 1. `JSONResponse`

* Explicitly returns JSON data.
* Useful when you want to control headers, status code, or content.
* It automatically converts Python dicts/lists into JSON.

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/json-example")
def json_example():
    data = {"message": "Hello, JSON!"}
    return JSONResponse(content=data, status_code=200)
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"message": "Hello, JSON!"}
```

---

## 2. `HTMLResponse`

* Returns an HTML document instead of JSON.
* Useful for serving webpages or templates directly.

```python
from fastapi.responses import HTMLResponse

@app.get("/html-example")
def html_example():
    html_content = """
    <html>
        <head><title>FastAPI Page</title></head>
        <body><h1>Hello, HTML!</h1></body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<html> ... </html>
```

---

## 3. `RedirectResponse`

* Redirects the client to another URL.
* Commonly used after login, form submission, or moved endpoints.

```python
from fastapi.responses import RedirectResponse

@app.get("/redirect-example")
def redirect_example():
    return RedirectResponse(url="/json-example")
```

**Response**

```http
HTTP/1.1 307 Temporary Redirect
Location: /json-example
```

---

## When to use which?

* **`JSONResponse`** → APIs returning structured data.
* **`HTMLResponse`** → Serving HTML content, maybe with Jinja templates.
* **`RedirectResponse`** → Redirect flows (login → dashboard, etc.).

---

✅ In short:

* `JSONResponse` → API data.
* `HTMLResponse` → Webpages.
* `RedirectResponse` → Navigation/redirect.
