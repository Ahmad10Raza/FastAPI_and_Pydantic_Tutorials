
### 1. Field Validation with Type Hints

Pydantic relies on **Python type hints** to automatically validate input data.

When you create a `BaseModel`, every field has a declared type, and Pydantic will enforce it.

---

#### Example 1: Basic Types

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int          # must be an integer
    name: str        # must be a string
    is_active: bool  # must be True/False

# ✅ Valid
user = User(id=1, name="Ahmad", is_active=True)
print(user)

# ❌ Invalid (wrong type)
try:
    user = User(id="abc", name=123, is_active="yes")
except Exception as e:
    print(e)
```

**Output (Validation Errors):**

```
3 validation errors for User
id
  Input should be a valid integer [type=int_parsing, input_value='abc', input_type=str]
name
  Input should be a valid string [type=string_type, input_value=123, input_type=int]
is_active
  Input should be a valid boolean [type=bool_parsing, input_value='yes', input_type=str]
```

---

#### Example 2: Lists and Dictionaries

```python
from typing import List, Dict

class Product(BaseModel):
    name: str
    tags: List[str]       # must be a list of strings
    attributes: Dict[str, str]  # key:value must be str:str

# ✅ Valid
product = Product(
    name="Laptop",
    tags=["electronics", "computer"],
    attributes={"brand": "Dell", "cpu": "i7"}
)

print(product)

# ❌ Invalid
try:
    product = Product(
        name="Laptop",
        tags="electronics",   # not a list
        attributes={"brand": 123}  # value must be str
    )
except Exception as e:
    print(e)
```

**Output:**

```
2 validation errors for Product
tags
  Input should be a valid list [type=list_type, input_value='electronics', input_type=str]
attributes.brand
  Input should be a valid string [type=string_type, input_value=123, input_type=int]
```

---

### Key Takeaways

* Pydantic uses **type hints** as validation rules.
* If the input data type doesn’t match, Pydantic raises  **ValidationError** .
* Works with:
  * Primitive types (`int`, `str`, `bool`, `float`)
  * Collections (`List`, `Dict`, `Tuple`, `Set`)
  * Nested models


---



### **Custom Validation in Pydantic**

Sometimes, just type hints (`int`, `str`, etc.) are not enough. You may need **custom rules** like:

* Ensuring an email has `@`
* Password must be at least 8 characters
* Age must be within a range

For such cases, Pydantic allows you to write  **custom validation logic** .

---

### **1. Pydantic v1: `@validator`**

In  **Pydantic v1** , you use `@validator` on a class method.

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    age: int

    @validator("age")
    def check_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value

user = User(name="Ahmad", age=20)
print(user)

# user = User(name="Ali", age=15)  # ❌ raises ValidationError
```

* `@validator("age")` → This runs whenever `age` is set.
* `cls` = class, `value` = field’s value.
* You must return the validated value, otherwise the field won’t be set.

---

### **2. Pydantic v2: `@field_validator`**

In  **Pydantic v2** , `@validator` was replaced with `@field_validator`.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def check_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value

user = User(name="Ahmad", age=22)
print(user)

# user = User(name="Ali", age=15)  # ❌ ValidationError
```

Notice differences:

* `@field_validator("age")` instead of `@validator`.
* You must add `@classmethod` in v2.

---

### **3. Multiple Fields Validation**

Sometimes validation depends on  **more than one field** . In that case:

* **v1:** Use `@root_validator`
* **v2:** Use `@model_validator`

Example (v2):

```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

---

✅ **Summary**

* v1 → `@validator` for fields, `@root_validator` for multiple fields.
* v2 → `@field_validator` for fields, `@model_validator` for multiple fields.

---
