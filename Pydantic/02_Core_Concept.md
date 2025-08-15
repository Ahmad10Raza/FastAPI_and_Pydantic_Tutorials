
### **Basic Model Creation**

At the heart of Pydantic is the **`BaseModel`** class.
You define data models by subclassing `BaseModel` and using **Python type hints** for fields.

---

#### 1. **Defining models using `BaseModel`**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
```

- Each attribute is **type-annotated** (`id: int`, `name: str`, etc.).
- Pydantic will validate and enforce types automatically.

---

#### 2. **Type hints for fields**

Pydantic leverages **Python type hints** to validate data:

```python
user = User(id="1", name="Alice", email="alice@example.com", age="25")
print(user)
```

Output:

```
id=1 name='Alice' email='alice@example.com' age=25
```

Even though you passed `"1"` (string) and `"25"` (string), Pydantic automatically **parses and converts** them into integers.
This is called **data parsing**.

If invalid data is provided:

```python
invalid_user = User(id="abc", name="Bob", email="bob@example.com", age=30)
```

Error:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for User
id
  Input should be a valid integer [type=int_type, input_value='abc', input_type=str]
```

---

#### 3. **Default values**

You can assign default values to fields:

```python
class Product(BaseModel):
    id: int
    name: str
    price: float = 99.99   # default value
    in_stock: bool = True  # default value

product = Product(id=1, name="Laptop")
print(product)
```

Output:

```
id=1 name='Laptop' price=99.99 in_stock=True
```

Defaults are applied when values are **not provided**.

---

✅ **Summary**

- `BaseModel` is the foundation of Pydantic models.
- Type hints drive validation and parsing.
- Defaults allow optional fields without extra code.


---

### **How Pydantic Parses Data**

Pydantic’s core job is to  **take raw input (dict, JSON, etc.) and convert it into strongly typed Python objects** .

* Input can be:
  * A Python `dict`
  * A JSON string
  * A nested structure (dict with dicts, lists, etc.)
* Pydantic:
  1. Checks **field names** in the `BaseModel`.
  2. Uses **type hints** to convert input into the correct type.
  3. Raises **validation errors** if parsing fails.

---

### **Example: Parsing dict into Pydantic Model**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int

# Raw data as dict
raw_data = {"id": "101", "name": "Alice", "age": "25"}  

user = User(**raw_data)  
print(user)            # id=101 name='Alice' age=25
print(user.id, type(user.id))  # 101 <class 'int'>
```

🔹 Even though `"id"` and `"age"` were strings, Pydantic **converted them into integers** automatically.

---

### **Parsing from JSON**

```python
import json

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

# JSON string
json_data = '{"name": "Laptop", "price": "799.99", "in_stock": "true"}'

# Parse JSON -> dict -> Pydantic Model
product = Product.model_validate_json(json_data)

print(product)
# name='Laptop' price=799.99 in_stock=True
```

Pydantic automatically  **parses string "true" → Python `True`** , `"799.99" → float`.

---

### **Validation Errors**

If input data does not match the type, Pydantic raises a detailed error.

```python
from pydantic import BaseModel, ValidationError

class Employee(BaseModel):
    id: int
    name: str
    salary: float

try:
    emp = Employee(id="abc", name=123, salary="ten thousand")
except ValidationError as e:
    print(e.json(indent=2))
```

Output:

```json
[
  {
    "loc": ["id"],
    "msg": "Input should be a valid integer",
    "type": "int_parsing"
  },
  {
    "loc": ["name"],
    "msg": "Input should be a valid string",
    "type": "string_type"
  },
  {
    "loc": ["salary"],
    "msg": "Input should be a valid number",
    "type": "float_parsing"
  }
]
```

---

✅ So Pydantic ensures:

* **Automatic conversion** (string → int, str → bool, etc.)
* **Strict validation** with clear error messages
* Works with **dict** and **JSON** seamlessly
