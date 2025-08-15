
---

### **What is FastAPI and why use it?**

FastAPI is a **modern, high-performance, Python web framework** designed for building APIs.

It stands out because it combines **speed, developer productivity, and data validation** seamlessly.

---

#### 1. **Modern, fast, async Python web framework**

* Built with **asynchronous programming** in mind (`async` / `await`).
* Extremely fast due to being built on top of **Starlette** (for web handling) and **Pydantic** (for data validation).
* One of the fastest Python frameworks, close to Node.js and Go in benchmarks.
* Supports both **sync** and **async** code, giving flexibility.

---

#### 2. **Built on ASGI (Starlette) + Pydantic**

* **ASGI (Asynchronous Server Gateway Interface):**
  * Successor of WSGI (used in Flask/Django).
  * Supports  **async I/O** , which is crucial for handling thousands of concurrent requests.
  * Enables features like WebSockets, background tasks, and real-time apps.
* **Starlette:** Lightweight ASGI toolkit for web handling (routing, middleware, sessions, etc.).
* **Pydantic:** Provides automatic request validation, parsing, and response serialization using type hints.

This means:

* When you define a request body or query parameter with type hints, FastAPI validates it automatically.
* Response models also use Pydantic for guaranteed schema correctness.

---

#### 3. **Advantages over Flask/Django for APIs**

* **Automatic validation & serialization**
  * In Flask/Django, you must manually validate input data.
  * In FastAPI, just define a Pydantic model and validation happens automatically.
* **Automatic API documentation**
  * Generates interactive API docs (`Swagger UI` & `ReDoc`) instantly.
  * No extra code needed for docs.
* **Speed & async support**
  * Flask and Django are sync-first frameworks (though Django has async support now).
  * FastAPI is async-native, making it more scalable.
* **Developer experience**
  * Full type hints support, better editor autocompletion, and fewer bugs.
  * Rapid prototyping with minimal code.
* **Microservices & modern APIs**
  * Great for REST APIs, GraphQL, and microservices.
  * Can integrate with Docker, Kubernetes, and modern DevOps setups easily.

---

👉 In short:

FastAPI =  **Starlette (web layer) + Pydantic (data validation) + Async Python** .

* [ ] It’s designed to be  **fast, developer-friendly, and production-ready** .

---



### 1. Install FastAPI and Uvicorn (Python Package Manager)

#### Using pip (most common):

```bash
pip install fastapi uvicorn
```

If you’re using Python 3 on Ubuntu, you may want to use:

```bash
pip3 install fastapi uvicorn
```

#### Using uv (modern package manager):

```bash
uv add fastapi uvicorn
```

---

### 2. Create a simple FastAPI app (`main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

---

### 3. Run the server with Uvicorn

```bash
uvicorn main:app --reload
```

Explanation:

* `main` → the filename (`main.py`)
* `app` → the FastAPI instance (`app = FastAPI()`)
* `--reload` → auto-restart on code changes (useful for development)

---

### 4. Access the API

* Root endpoint: [http://127.0.0.1:8000](http://127.0.0.1:8000/)
* Interactive docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Alternative docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
