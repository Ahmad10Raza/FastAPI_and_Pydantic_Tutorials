
## JSON Serialization & Deserialization in Pydantic

Pydantic makes it very easy to move between **Python objects** and  **JSON data** .

---

### 1. **Serialization** (Python object → JSON)

Serialization means converting a **Pydantic model** into JSON (string or dict) so it can be stored or sent via APIs.

#### Example

```python
from pydantic import BaseModel
import json

class User(BaseModel):
    id: int
    name: str
    email: str

# Create a Python object
user = User(id=1, name="Ahmad", email="ahmad@example.com")

# Convert to dict
print(user.model_dump())
# {'id': 1, 'name': 'Ahmad', 'email': 'ahmad@example.com'}

# Convert to JSON string
print(user.model_dump_json())
# {"id":1,"name":"Ahmad","email":"ahmad@example.com"}

# Using json library explicitly
json_string = json.dumps(user.model_dump())
print(json_string)
```

Key methods:

* `model_dump()` → returns a  **Python dict** .
* `model_dump_json()` → returns a  **JSON string** .

---

### 2. **Deserialization** (JSON → Python object)

Deserialization means converting a **JSON string/dict** into a Pydantic model.

#### Example

```python
# JSON string from an API
json_data = '{"id": 2, "name": "Sara", "email": "sara@example.com"}'

# Convert JSON string → dict
parsed_dict = json.loads(json_data)

# Parse dict into Pydantic model
user2 = User(**parsed_dict)
print(user2)
# id=2 name='Sara' email='sara@example.com'
```

---

### 3. **Working directly with `parse_raw` and `model_validate_json`**

Instead of manually calling `json.loads`, Pydantic has built-in helpers.

#### Example

```python
# JSON string
json_data = '{"id": 3, "name": "Ali", "email": "ali@example.com"}'

# Parse raw JSON into model
user3 = User.model_validate_json(json_data)
print(user3)
# id=3 name='Ali' email='ali@example.com'
```

---

### 4. **Serialization with customization**

You can control how data is serialized (for example, converting datetime to ISO string).

```python
from datetime import datetime

class Event(BaseModel):
    id: int
    timestamp: datetime

event = Event(id=101, timestamp=datetime.now())

# Default JSON serialization
print(event.model_dump_json())
# {"id":101,"timestamp":"2025-08-14T12:45:32.123456"}
```

---

### Summary

* **Serialization** :
* `model_dump()` → dict
* `model_dump_json()` → JSON string
* **Deserialization** :
* `Model(**data_dict)`
* `Model.model_validate_json(json_string)`
* Supports **complex types** like `datetime`, `UUID`, `Decimal` automatically.


---



## Handling Environment Variables with `BaseSettings`

Pydantic provides a class called  **`BaseSettings`** , which is designed to manage application configuration using **environment variables** (and `.env` files).

This is very useful for:

* Secrets (API keys, passwords, tokens)
* Database URLs
* Environment-specific configs (dev, staging, prod)

---

### 1. **Basic Example**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"  # Optional: load from .env file

# Load settings
settings = Settings()

print(settings.app_name)
print(settings.debug)
print(settings.database_url)
```

If you set environment variables like:

```bash
export APP_NAME="CoolApp"
export DEBUG="true"
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

Then run Python:

```python
print(settings.app_name)   # CoolApp
print(settings.debug)      # True
print(settings.database_url)  # postgresql://user:pass@localhost/db
```

---

### 2. **Using `.env` files**

You don’t always want to export env vars manually. Instead, you can keep them in a `.env` file.

**.env file**

```
APP_NAME=EnvApp
DEBUG=true
DATABASE_URL=sqlite:///./test.db
```

Pydantic will automatically read this file (since we set `env_file = ".env"` in `Config`).

```python
print(settings.app_name)      # EnvApp
print(settings.debug)         # True
print(settings.database_url)  # sqlite:///./test.db
```

---

### 3. **Customizing Environment Variable Names**

You can override field names with `env` in `Field`.

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    db_url: str = Field(..., env="DATABASE_URL")  # map to DATABASE_URL env var
    api_key: str = Field(..., env="MY_APP_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()
print(settings.db_url)
print(settings.api_key)
```

---

### 4. **Nested Environment Variables**

Pydantic supports nested settings via dot notation.

```python
from pydantic_settings import BaseSettings
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = 10

class Settings(BaseSettings):
    database: DatabaseConfig

    class Config:
        env_file = ".env"
        env_nested_delimiter = '__'  # double underscore separates nested fields

# Example .env file
"""
DATABASE__URL=postgresql://localhost/mydb
DATABASE__POOL_SIZE=20
"""

settings = Settings()
print(settings.database.url)       # postgresql://localhost/mydb
print(settings.database.pool_size) # 20
```

---

### 5. **Priority of values**

Pydantic loads config in this order (highest → lowest priority):

1. Arguments passed directly to `Settings()`
2. Environment variables
3. `.env` file
4. Default values in the model

---

### 6. **Serialization for Debugging**

You can check all loaded settings easily:

```python
print(settings.model_dump())
```

---

✅  **In short** :

* Use `BaseSettings` for config management.
* Supports  **env vars + .env files** .
* `env_nested_delimiter` helps manage structured configs.
* Good for **12-factor apps** (config outside code).
