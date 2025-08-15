
### 1. **Foundations of REST**

* What is an API?
* What is REST (Representational State Transfer)?
* REST principles:
  * Client-server architecture
  * Statelessness
  * Cacheability
  * Uniform interface (resources and URIs)
  * Layered system
* REST vs SOAP vs GraphQL

---

### 2. **HTTP Basics (Backbone of REST APIs)**

* HTTP request/response cycle
* HTTP methods (verbs):
  * GET (read)
  * POST (create)
  * PUT/PATCH (update)
  * DELETE (remove)
* HTTP status codes:
  * 1xx (informational)
  * 2xx (success: 200, 201, 204)
  * 3xx (redirection: 301, 302)
  * 4xx (client errors: 400, 401, 403, 404)
  * 5xx (server errors: 500, 502)
* Request headers & response headers
* Content-Type, Accept headers (JSON, XML, etc.)

---

### 3. **REST API Design**

* Resource naming conventions (nouns not verbs, plural form)
  * `/users`, `/users/{id}`
* Query parameters vs Path parameters
* Pagination, filtering, sorting (`?page=2&limit=20`)
* Versioning APIs (`/api/v1/...`)
* Idempotency (safe vs unsafe methods)

---

### 4. **Data Formats & Serialization**

* JSON (default for REST APIs)
* XML (legacy support)
* YAML (sometimes used)
* Request body & Response body basics

---

### 5. **API Security**

* Authentication vs Authorization
* Basic Auth
* API keys
* OAuth2 & JWT (JSON Web Tokens)
* Rate limiting & throttling
* CORS (Cross-Origin Resource Sharing)

---

### 6. **Error Handling & Responses**

* Standard error format (with `code`, `message`, `details`)
* Using proper status codes
* Custom error responses

---

### 7. **Documentation**

* OpenAPI / Swagger (auto-generated docs)
* Postman collections
* API versioning strategies

---

### 8. **Testing REST APIs**

* Manual testing with:
  * cURL
  * Postman / Insomnia
* Automated testing with:
  * Python (pytest + requests)
  * JavaScript (Jest + Supertest)

---

### 9. **Practical Implementation**

* Building a simple REST API in:
  * Python (Flask, FastAPI, Django REST Framework)
  * Node.js (Express.js)
* CRUD operations example (users, tasks, products)
* Database integration (SQL & NoSQL)

---

### 10. **Advanced Concepts**

* HATEOAS (Hypermedia as the Engine of Application State)
* Rate limiting & API throttling
* Logging & monitoring APIs
* Deploying REST APIs (Docker, AWS, Azure, GCP)

---
