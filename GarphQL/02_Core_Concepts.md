
---

### 1. **Schema in GraphQL**

* A **schema** defines the structure of data available to the client.
* It acts as a contract between the **client** and  **server** .
* Written in the  **GraphQL Schema Definition Language (SDL)** .
* It tells:
  * What queries are possible
  * What data types exist
  * Relationships between types

Example schema snippet:

```graphql
type Query {
  user(id: ID!): User
  posts: [Post]
}
```

Here:

* `user` and `posts` are queries.
* `User` and `Post` are object types.

---

### 2. **Scalar Types**

Scalars are the **basic, indivisible types** in GraphQL.

* **Int** → Integer value (32-bit signed)
  ```graphql
  age: Int
  ```
* **Float** → Decimal number
  ```graphql
  rating: Float
  ```
* **String** → Text data
  ```graphql
  name: String
  ```
* **Boolean** → True/False value
  ```graphql
  isActive: Boolean
  ```
* **ID** → Unique identifier, often used for objects
  ```graphql
  id: ID!
  ```

(`!` means the field is  **non-nullable** , it must always return a value.)

---

### 3. **Custom Types**

You can define your own types beyond scalars.

* **Enums** → A restricted set of possible values
  ```graphql
  enum Role {
    ADMIN
    USER
    GUEST
  }
  ```
* **Input Types** → Used for sending structured input to mutations
  ```graphql
  input UserInput {
    name: String!
    email: String!
  }
  ```

---

### 4. **Object Types**

* These are the **core building blocks** of GraphQL schemas.
* Define a set of fields and their return types.
* Example:
  ```graphql
  type User {
    id: ID!
    name: String!
    email: String!
    role: Role
  }

  type Post {
    id: ID!
    title: String!
    content: String
    author: User
  }
  ```

Here:

* `User` and `Post` are object types.
* `Post` has a field `author` that links to the `User` type → shows how GraphQL handles  **relationships** .

---

✅ **Summary**

* Scalars → basic data types (Int, Float, String, Boolean, ID).
* Custom types → Enums, Input objects, etc.
* Object types → define real-world entities with fields and relationships.
* Schema ties everything together and defines what clients can query.


---

### 1. Structure of a GraphQL Query

A query looks like the shape of the data you want.

Example:

```graphql
query {
  user(id: "101") {
    id
    name
    email
  }
}
```

* `query`: keyword indicating you are requesting data.
* `user(id: "101")`: field with an argument (fetch user with id `101`).
* `{ id name email }`: subfields requested from the `user` object.

Response:

```json
{
  "data": {
    "user": {
      "id": "101",
      "name": "Alice",
      "email": "alice@example.com"
    }
  }
}
```

Notice how the  **response matches the shape of the query** .

---

### 2. Query with Multiple Fields

You can request data from multiple fields in a single query.

```graphql
query {
  user(id: "101") {
    name
  }
  posts {
    title
    author {
      name
    }
  }
}
```

---

### 3. Query with Arguments

Arguments make queries dynamic.

```graphql
query {
  post(id: "202") {
    title
    content
  }
}
```

---

### 4. Aliases

Aliases allow renaming fields, useful when calling the same field multiple times with different arguments.

```graphql
query {
  firstUser: user(id: "101") {
    name
  }
  secondUser: user(id: "102") {
    name
  }
}
```

---

### 5. Variables

Instead of hardcoding arguments, you can pass **variables** for flexibility.

```graphql
query getUser($userId: ID!) {
  user(id: $userId) {
    name
    email
  }
}
```

With variables:

```json
{
  "userId": "101"
}
```

---

### 6. Nested Queries

You can fetch related/nested data in one request.

```graphql
query {
  user(id: "101") {
    name
    posts {
      title
      comments {
        content
      }
    }
  }
}
```

---

### 7. Fragments

Fragments allow reusing common fields across queries.

```graphql
fragment userFields on User {
  id
  name
  email
}

query {
  user(id: "101") {
    ...userFields
  }
  anotherUser: user(id: "102") {
    ...userFields
  }
}
```

---

✅ Key takeaways:

* GraphQL queries let clients fetch  **exactly the required data** .
* They support arguments, aliases, variables, nesting, and fragments.
* Queries reduce over-fetching and under-fetching compared to REST.



### **Mutations in GraphQL**

In GraphQL, **mutations** are used to perform write operations, such as creating, updating, or deleting data. Unlike queries (which are read-only), mutations modify server-side data and usually return a response containing the updated data.

---

### **1. Performing Write Operations**

* A **mutation** is defined in the schema alongside queries.
* Mutations are similar to queries in syntax but are prefixed with the keyword `mutation`.
* Each mutation can return data, often the newly created/updated object or a confirmation.

**Example: Adding a new user**

```graphql
mutation {
  createUser(name: "Ahmad", email: "ahmad@example.com") {
    id
    name
    email
  }
}
```

**Explanation**

* `createUser` is the mutation name.
* We pass `name` and `email` as arguments.
* The response requests `id`, `name`, and `email` of the created user.

---

### **2. Arguments in Mutations**

* Mutations accept arguments like queries, allowing fine-grained control over the data.
* Arguments can be simple scalars (`String`, `Int`) or complex input objects.

**Example: Updating a user's email**

```graphql
mutation {
  updateUser(id: 1, email: "newmail@example.com") {
    id
    name
    email
  }
}
```

Here:

* `id` identifies the user to update.
* `email` is the new value.

---

### **3. Input Types**

Instead of passing multiple arguments individually, GraphQL allows grouping them into  **input types** , which improves readability and reusability.

**Schema Example:**

```graphql
input CreateUserInput {
  name: String!
  email: String!
}

type Mutation {
  createUser(input: CreateUserInput!): User
}
```

**Mutation Example:**

```graphql
mutation {
  createUser(input: { name: "Ahmad", email: "ahmad@example.com" }) {
    id
    name
    email
  }
}
```

---

✅ **Key Takeaways**

* **Mutations** are for write operations (create, update, delete).
* They look like queries but start with the `mutation` keyword.
* They can take **arguments** or structured **input types** for better scalability.
* Mutations return data, so clients can immediately confirm the change.


### 1. Subscriptions in GraphQL

* **Definition** : Subscriptions allow clients to receive **real-time updates** from the server whenever certain events happen (e.g., new messages, live stock updates, sensor data).
* Instead of pulling data repeatedly (polling), the server **pushes updates** to subscribed clients automatically.

---

### 2. How Subscriptions Work

* A client subscribes to an event using a **subscription query** (similar to how queries/mutations are written).
* The server listens for those events and notifies all subscribed clients when the event occurs.

 **Example** :

```graphql
subscription {
  newMessage {
    id
    content
    sender
  }
}
```

* This means the client wants to be notified whenever a **newMessage** event happens.
* When a new message is added (through a mutation), the server pushes the new message details to all subscribed clients.

---

### 3. Real-time Data with WebSockets

* Unlike queries and mutations (which usually run over HTTP), **subscriptions use WebSockets** to maintain a persistent two-way connection between client and server.
* This allows the server to send data updates instantly without waiting for the client to request again.

 **Flow** :

1. Client opens a WebSocket connection to the GraphQL server.
2. Client sends a subscription query.
3. Server keeps the connection open and listens for events.
4. When an event occurs (e.g., new data), server sends the update to the client in real time.

---

### 4. Use Cases of Subscriptions

* **Chat applications** → real-time messaging
* **Live dashboards** → financial markets, IoT sensors
* **Notifications** → system alerts, collaboration tools
* **Collaborative editing** → Google Docs–like real-time collaboration

---

✅ In short:

* **Queries** → fetch data (read once).
* **Mutations** → change data (write).
* **Subscriptions** → listen for real-time updates (continuous).
