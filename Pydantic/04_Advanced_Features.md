
### 🔹 What are Nested Models?

* A **nested model** means having one `BaseModel`  **inside another model** .
* This is useful when your data has a  **hierarchical structure** , such as a **User** having an  **Address** , or an **Order** containing multiple  **Items** .

---

### 🔹 Example 1: Simple Nested Model

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class User(BaseModel):
    name: str
    age: int
    address: Address  # Nested model here!

# Input data
data = {
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zipcode": "10001"
    }
}

user = User(**data)
print(user)
print(user.address.city)
```

✅ Output:

```
name='Alice' age=30 address=Address(street='123 Main St', city='New York', zipcode='10001')
New York
```

* Pydantic  **automatically parses the inner dictionary into an `Address` object** .

---

### 🔹 Example 2: Nested Model with Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)  # price must be > 0

class Order(BaseModel):
    id: int
    items: list[Item]  # List of nested models

order_data = {
    "id": 101,
    "items": [
        {"name": "Laptop", "price": 999.99},
        {"name": "Mouse", "price": 25.50},
    ]
}

order = Order(**order_data)
print(order)
print(order.items[0].name)
```

✅ Output:

```
id=101 items=[Item(name='Laptop', price=999.99), Item(name='Mouse', price=25.5)]
Laptop
```

* Each dictionary inside `items` is automatically validated and converted into an `Item` object.

---

### 🔹 Example 3: Handling Validation Errors in Nested Models

```python
invalid_order_data = {
    "id": 102,
    "items": [
        {"name": "Keyboard", "price": -50},  # ❌ Invalid price
    ]
}

try:
    order = Order(**invalid_order_data)
except Exception as e:
    print(e)
```

✅ Output:

```
1 validation error for Order
items.0.price
  Input should be greater than 0 [type=greater_than, input_value=-50, gt=0]
```

* Error messages clearly show  **which nested field failed** .

---

### 🔑 Key Takeaways

* Nested models let you  **organize complex data structures** .
* Pydantic  **automatically parses and validates inner dictionaries/lists** .
* Validation errors are **deeply traced** (it tells you exactly where the error is, even inside nested objects).

---


## 1. **Optional Types**

In Python typing:

* `Optional[X]` means the value can be of type `X` or `None`.
* It is shorthand for `Union[X, None]`.

### Example

```python
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None  # email may or may not be provided

# Case 1: email provided
u1 = User(id=1, name="Alice", email="alice@example.com")
print(u1)

# Case 2: email missing
u2 = User(id=2, name="Bob")
print(u2)
```

✅ Pydantic allows both with and without `email`, since it’s optional.

---

## 2. **Union Types**

* `Union[A, B]` means the field can be either type `A` or type `B`.
* Useful when the data format can vary.

### Example

```python
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    id: Union[int, str]   # can be int or string
    price: float

# Case 1: int id
i1 = Item(id=101, price=99.9)
print(i1)

# Case 2: str id
i2 = Item(id="SKU-123", price=49.5)
print(i2)
```

✅ Both integer and string work for `id`.

---

## 3. **Mixing Optional + Union**

You can combine them:

```python
from typing import Union, Optional
from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    discount: Optional[Union[int, float]] = None  
    # discount can be int, float, or None

o1 = Order(order_id=1, discount=10)
o2 = Order(order_id=2, discount=5.5)
o3 = Order(order_id=3)  # no discount
```

---

## 4. **Validation Behavior**

Pydantic will:

* Try to **coerce** values into the allowed types (e.g., `"123"` → `int` if `Union[int, str]`).
* Raise a **validation error** if the value doesn’t match any type.

### Example

```python
Item(id=[1,2,3], price=20.0)
```

❌ Raises error because `list` is not allowed for `id`.



---

### 1. **Why Aliases Are Useful?**

Sometimes the input data (e.g., from JSON, API, or DB) may not follow Python’s naming conventions or may use different field names.

* Example: The API sends `"user_name"` but in Python, you prefer `username`.
* Aliases let you map between **external field names** and  **internal Python attributes** .

---

### 2. **Using `Field` with `alias`**

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., alias="user_name")
    age: int

# Input data with alias
data = {"user_name": "ahmad", "age": 22}

user = User(**data)

print(user.username)   # ahmad
print(user.age)        # 22
```

* `Field(..., alias="user_name")` means:
  * Externally (when parsing), Pydantic expects `"user_name"`.
  * Internally (when accessing in Python), you use `user.username`.

---

### 3. **Exporting with Aliases**

When you serialize (`.model_dump()`), by default, it uses the Python attribute names.

To output using aliases, use `by_alias=True`.

```python
print(user.model_dump())  
# {'username': 'ahmad', 'age': 22}

print(user.model_dump(by_alias=True))  
# {'user_name': 'ahmad', 'age': 22}
```

---

### 4. **Other Field Customization Options**

The `Field()` function lets you control extra behavior of a field:

* **Default values with metadata**

```python
class Product(BaseModel):
    name: str
    price: float = Field(0, description="Price of the product in USD")
```

* **Constraints**

```python
class Account(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., ge=18, le=99)  # ge = >=, le = <=
```

* **Examples**

```python
class Item(BaseModel):
    name: str = Field(..., example="Laptop")
    quantity: int = Field(..., example=10)
```

---

### 5. **Summary**

* `alias="..."` → maps external names to internal Python attributes.
* `model_dump(by_alias=True)` → export using aliases.
* `Field()` → allows constraints (length, range), metadata (description, example), and better control over fields.


---

### **What are Computed Fields?**

* In Pydantic  **v2** , a *computed field* is a **read-only field** whose value is not stored directly but is **calculated dynamically** from other fields in the model.
* It is defined using the `@computed_field` decorator.

This is useful when you want:

* Derived properties (like `full_name` from `first_name` + `last_name`).
* Data that depends on other fields, without storing it redundantly.

---

### **Example**

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    first_name: str
    last_name: str
  
    @computed_field  # This makes it part of the model output
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

# Example usage
user = User(first_name="John", last_name="Doe")
print(user.full_name)   # John Doe
print(user.model_dump())  
```

**Output:**

```python
{
    'first_name': 'John',
    'last_name': 'Doe',
    'full_name': 'John Doe'   # included automatically
}
```

---

### **Key Points**

* `@computed_field` must be applied  **on top of `@property`** .
* The return type must be annotated (e.g., `-> str`).
* Computed fields are included in:
  * `model_dump()`
  * JSON serialization (`model_dump_json()`)
* They are  **read-only** : you cannot set them directly.

---

### **Customization**

You can configure the computed field with options inside the decorator:

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float
  
    @computed_field(alias="area_sq_units")  # custom alias
    @property
    def area(self) -> float:
        return self.width * self.height

rect = Rectangle(width=5, height=10)
print(rect.model_dump())
```

**Output:**

```python
{'width': 5.0, 'height': 10.0, 'area_sq_units': 50.0}
```

---

✅ **Difference from normal `@property`:**

* Normal `@property` does not appear in `model_dump()` or JSON serialization.
* `@computed_field` integrates with Pydantic’s serialization system.




---

## **1. Strict Mode**

By default, Pydantic is permissive and tries to coerce values into the right type. Strict mode forces exact type matching.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)   # Enable strict mode
    age: int

# Example
print(User(age=25))      # ✅ Works
print(User(age="25"))    # ❌ Error: str is not accepted as int
```

* **Without strict mode** → `"25"` would be coerced into `25`.
* **With strict mode** → Validation error if type does not match.

---

## **2. Allow Extra Fields**

By default, extra fields in input raise an error. You can configure how they’re handled.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")  # options: "ignore", "forbid", "allow"
    name: str

# Example
print(User(name="Alice", age=30))  
# extra="ignore" → ✅ age ignored
# extra="allow"  → ✅ age stored but not in schema
# extra="forbid" → ❌ Validation error
```

* `"ignore"`: Extra fields are dropped.
* `"forbid"`: Validation error if extra fields are present.
* `"allow"`: Extra fields are stored in model, accessible via `.model_extra`.

---

## **3. Serialization Rules**

Serialization controls  **how models convert to JSON or dict** .

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Event(BaseModel):
    model_config = ConfigDict(
        ser_json_timedelta="iso8601",  # Serialization formatting
        ser_json_timedelta_as="float"
    )
    name: str
    timestamp: datetime

event = Event(name="Launch", timestamp=datetime(2025, 8, 14, 10, 30))
print(event.model_dump())      # Python dict
print(event.model_dump_json()) # JSON string
```

Common serialization options:

* `str_to_lower=True` → lowercase all strings.
* `ser_json_timedelta="iso8601"` → format timedeltas in ISO 8601.
* `populate_by_name=True` → allow serialization with field names and aliases.

---

### Example Combining All:

```python
class Product(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="ignore",
        populate_by_name=True
    )
    id: int
    price: float
    in_stock: bool
```

```python
data = {"id": "101", "price": 10.5, "in_stock": "true", "extra_field": "ignore me"}
product = Product(**data)  # ❌ Will fail since strict=True
```
