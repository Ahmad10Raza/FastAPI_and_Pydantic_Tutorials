
### 1. What is a GraphQL Schema?

* A **schema** defines the **structure of data** in a GraphQL API.
* It describes:
  * What types of data are available.
  * How clients can  **query** ,  **mutate** , or **subscribe** to that data.
* The schema is written in  **SDL (Schema Definition Language)** .

Think of it as the **blueprint** of your API.

---

### 2. Key Building Blocks of a Schema

1. **Types**
   * Used to describe the shape of data.
   * Example:

     ```graphql
     type User {
       id: ID!
       name: String!
       email: String!
     }
     ```

     * `ID!` means non-null unique identifier.
     * `String!` means required string.
2. **Query Type**
   * Defines how clients  **read data** .
   * Example:

     ```graphql
     type Query {
       getUser(id: ID!): User
       listUsers: [User!]!
     }
     ```

     * `getUser` returns a single user by ID.
     * `listUsers` returns a list of users.
3. **Mutation Type**
   * Defines how clients  **write/update data** .
   * Example:
     ```graphql
     type Mutation {
       createUser(name: String!, email: String!): User!
       deleteUser(id: ID!): Boolean!
     }
     ```
4. **Subscription Type**
   * Defines how clients  **receive real-time updates** .
   * Example:
     ```graphql
     type Subscription {
       userAdded: User!
     }
     ```
5. **Input Types**
   * Used for passing complex objects as arguments to mutations.
   * Example:
     ```graphql
     input CreateUserInput {
       name: String!
       email: String!
     }

     type Mutation {
       createUser(input: CreateUserInput!): User!
     }
     ```

---

### 3. Schema Design Best Practices

* **Think in entities** : Identify the core objects (e.g., User, Product, Post).
* **Use clear and meaningful names** : Avoid vague field names.
* **Normalize relations** :
* Example: A `Post` should reference `User` instead of duplicating user info.
* **Use non-null (`!`) carefully** : Make required fields explicit.
* **Design queries for clients, not databases** :
* Avoid exposing unnecessary complexity.
* Provide the right balance of flexibility and simplicity.
* **Modularize schema** : Split into files/modules for large projects.

---

### 4. Example: Schema for a Blog

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  getUser(id: ID!): User
  listPosts: [Post!]!
}

input CreatePostInput {
  title: String!
  content: String!
  authorId: ID!
}

type Mutation {
  createPost(input: CreatePostInput!): Post!
}

type Subscription {
  postAdded: Post!
}
```

* `Query` → Fetch users and posts.
* `Mutation` → Create posts.
* `Subscription` → Get real-time updates when a new post is added.


---



In GraphQL, relationships between types define how different entities in your data connect to each other. Since real-world data is often interlinked (for example, a user has posts, a post has comments, etc.), GraphQL schemas must capture these relationships so clients can query across them easily.

### Types of Relationships in GraphQL

1. **One-to-One Relationship**
   * Example: A user has exactly one profile.
   * Schema:
     ```graphql
     type User {
       id: ID!
       name: String!
       profile: Profile
     }

     type Profile {
       id: ID!
       bio: String
       user: User
     }
     ```
2. **One-to-Many Relationship**
   * Example: A user can write many posts, but each post belongs to one user.
   * Schema:
     ```graphql
     type User {
       id: ID!
       name: String!
       posts: [Post!]!
     }

     type Post {
       id: ID!
       title: String!
       content: String
       author: User!
     }
     ```
3. **Many-to-Many Relationship**
   * Example: A student can enroll in many courses, and each course can have many students.
   * Schema:
     ```graphql
     type Student {
       id: ID!
       name: String!
       courses: [Course!]!
     }

     type Course {
       id: ID!
       title: String!
       students: [Student!]!
     }
     ```

### How Relationships Work with Queries

* GraphQL allows clients to traverse relationships naturally.
* Example query (User → Posts → Author):
  ```graphql
  query {
    users {
      name
      posts {
        title
        author {
          name
        }
      }
    }
  }
  ```

### Benefits of Defining Relationships

* Enables **nested queries** that fetch related data in one request.
* Improves **data representation** by modeling real-world entities.
* Supports  **flexibility** , allowing clients to choose exactly what data they need.


---

### 1. **Output Types**

* Used for **returning data** to the client in queries, mutations, or subscriptions.
* Defined with `type`.
* Can have fields that reference other types, scalars, lists, or even custom objects.

**Example**

```graphql
type User {
  id: ID!
  name: String!
  email: String!
}
```

Here, `User` is an  **output type** .

If a query asks for users, the server will return data shaped like `User`.

**Usage in Query**

```graphql
type Query {
  users: [User!]!
}
```

---

### 2. **Input Types**

* Used for **sending data from the client** into mutations or query arguments.
* Defined with `input`.
* Can only contain scalars, enums, and other input types (not output types).
* No resolvers inside — just a structured way to accept input.

**Example**

```graphql
input CreateUserInput {
  name: String!
  email: String!
}
```

**Usage in Mutation**

```graphql
type Mutation {
  createUser(data: CreateUserInput!): User!
}
```

Here, the client sends a `CreateUserInput` object to create a user, and the server returns a `User` object (output type).

---

### Key Differences

| Feature                | Output Type (`type`)            | Input Type (`input`)              |
| ---------------------- | --------------------------------- | ----------------------------------- |
| Purpose                | Returning data                    | Sending data to server              |
| Can contain resolvers? | Yes (via fields)                  | No                                  |
| Allowed fields         | Scalars, objects, lists           | Scalars, enums, other input types   |
| Used in                | Queries, Mutations, Subscriptions | Mutation arguments, Query arguments |

---

### Example in Practice

```graphql
# Output type
type Post {
  id: ID!
  title: String!
  content: String
}

# Input type
input CreatePostInput {
  title: String!
  content: String
}

type Mutation {
  createPost(data: CreatePostInput!): Post!
}
```

**Client Mutation Request**

```graphql
mutation {
  createPost(data: { title: "GraphQL Basics", content: "Learning input vs output types" }) {
    id
    title
  }
}
```

**Server Response**

```json
{
  "data": {
    "createPost": {
      "id": "101",
      "title": "GraphQL Basics"
    }
  }
}
```


---

### **1. Enum Types**

Enums (short for  *enumerations* ) are like predefined sets of constants.

They restrict a field to a specific set of allowed values.

* **Use Case** : When you want a field to accept only certain values.
* Example: Status of an order, user roles, or days of the week.

```graphql
enum OrderStatus {
  PENDING
  SHIPPED
  DELIVERED
  CANCELED
}

type Order {
  id: ID!
  product: String!
  status: OrderStatus!
}
```

* Here, `status` must be one of: `PENDING`, `SHIPPED`, `DELIVERED`, `CANCELED`.
* It helps avoid errors and ensures type safety.

---

### **2. Union Types**

Unions allow a field to return **different object types** (but not scalar or enum).

Unlike interfaces, unions don’t require the types to share common fields.

* **Use Case** : When a field can return different shapes of data.
* Example: A search query might return results of different types like `Book` or `Author`.

```graphql
union SearchResult = Book | Author

type Book {
  id: ID!
  title: String!
}

type Author {
  id: ID!
  name: String!
}

type Query {
  search(keyword: String!): [SearchResult!]!
}
```

* If you query `search("AI")`, the result may contain both `Book` and `Author` objects.
* On the client side, you check which type was returned using `__typename`.

Example query:

```graphql
query {
  search(keyword: "AI") {
    __typename
    ... on Book {
      title
    }
    ... on Author {
      name
    }
  }
}
```

---

✅ **Key Difference**

* **Enum** : Limits a field to specific scalar values.
* **Union** : Allows a field to return different object types.


---

### **1. Interfaces in GraphQL**

An **Interface** defines a set of common fields that multiple object types can implement.

Think of it as a contract: any type that implements an interface must include all its fields.

* **Use Case** : When multiple types share some fields, but also have unique ones.

Example:

```graphql
interface Character {
  id: ID!
  name: String!
}

type Hero implements Character {
  id: ID!
  name: String!
  superPower: String!
}

type Villain implements Character {
  id: ID!
  name: String!
  evilPlan: String!
}

type Query {
  characters: [Character!]!
}
```

* `Hero` and `Villain` both implement `Character`.
* When you query `characters`, you can request common fields from `Character`.
* To fetch specific fields, you use  **fragments** .

Query:

```graphql
query {
  characters {
    id
    name
    ... on Hero {
      superPower
    }
    ... on Villain {
      evilPlan
    }
  }
}
```

---

### **2. Inheritance in GraphQL**

GraphQL doesn’t have **class inheritance** like in OOP. Instead, it uses **interfaces** to achieve a similar effect:

* Common fields go in the  **interface** .
* Each **type implements** the interface and can add its own unique fields.
* This allows you to treat multiple types as one (polymorphism).

So, you can think of interfaces as a way to model **shared behavior** and achieve  **type safety** .

---

### **3. Interface vs Union**

They often get confused. Here’s the difference:

* **Interface** : Types must share some common fields.
* **Union** : Types don’t need to share anything in common, they’re just grouped.

Example:

* `Character` interface ensures all implementers have `id` and `name`.
* `SearchResult` union (Book | Author) doesn’t enforce shared fields.

---

⚡ **Quick Analogy**

* Interface → like a **base class** with required properties.
* Union → like saying “this can be one of these different shapes,” no common rules.
