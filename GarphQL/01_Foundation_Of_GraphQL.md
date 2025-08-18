
# What is GraphQL and how it differs from REST

GraphQL is a **query language** and **runtime** for APIs developed by Facebook in 2012 (open-sourced in 2015). It allows clients to request exactly the data they need, nothing more and nothing less. Unlike REST, where fixed endpoints return fixed data structures, GraphQL gives clients more flexibility and efficiency in fetching data.

### What is GraphQL?

* A **query language** for APIs: Clients define what data they want.
* A  **runtime** : Executes queries against your data.
* **Strongly typed** : Based on a schema that defines available data types and relationships.
* **Flexible and efficient** : Clients can query multiple resources in a single request.

---

### How GraphQL differs from REST

1. **Data Fetching**
   * **REST** : Requires multiple endpoints to fetch related data.
   * Example: `/users/1` → user details, `/users/1/posts` → user’s posts.
   * **GraphQL** : A single query can fetch user details and their posts in one request.
2. **Over-fetching & Under-fetching**
   * **REST** : Clients may receive unnecessary data (over-fetching) or not enough (under-fetching), requiring multiple requests.
   * **GraphQL** : Clients specify exactly what fields they want.
3. **Endpoints**
   * **REST** : Multiple endpoints for different resources (`/users`, `/posts`, `/comments`).
   * **GraphQL** : A single endpoint (`/graphql`) handles all queries.
4. **Response Structure**
   * **REST** : Server decides the structure of responses.
   * **GraphQL** : Client decides the shape of the response.
5. **Versioning**
   * **REST** : Often uses versioning (`/v1/users`, `/v2/users`).
   * **GraphQL** : No versioning needed; schema evolves by adding new fields while keeping old ones.
6. **Error Handling**
   * **REST** : Relies on HTTP status codes (`404`, `500`).
   * **GraphQL** : Errors are part of the response JSON.
7. **Performance**
   * **REST** : Multiple round-trips to the server.
   * **GraphQL** : Reduces network calls with a single optimized query.

---

### Example Comparison

**REST API Calls:**

```http
GET /user/1
{
  "id": 1,
  "name": "Ahmad"
}

GET /user/1/posts
[
  { "id": 101, "title": "GraphQL Intro" },
  { "id": 102, "title": "REST vs GraphQL" }
]
```

**GraphQL Query:**

```graphql
{
  user(id: 1) {
    name
    posts {
      title
    }
  }
}
```

**GraphQL Response:**

```json
{
  "data": {
    "user": {
      "name": "Ahmad",
      "posts": [
        { "title": "GraphQL Intro" },
        { "title": "REST vs GraphQL" }
      ]
    }
  }
}
```


# Benefits of GraphQL (single endpoint, strongly typed schema, avoids over/under-fetching)

### 1. **Single Endpoint**

- In **REST APIs**, you typically have multiple endpoints (e.g., `/users`, `/users/{id}`, `/users/{id}/posts`).
- In **GraphQL**, you expose just **one endpoint** (usually `/graphql`). All queries, mutations, and subscriptions are sent to this single endpoint.
- Benefit:
  - Simplifies API design and reduces endpoint sprawl.
  - Easier for clients to interact with the API since they always know where to send requests.

---

### 2. **Strongly Typed Schema**

- GraphQL APIs are defined by a **schema** written in the GraphQL Schema Definition Language (SDL).
- The schema specifies types, fields, and relationships between them.
- Benefit:
  - Acts as a contract between client and server.
  - Enables **auto-completion**, **introspection**, and **better developer tooling** (e.g., GraphiQL, Apollo Studio).
  - Helps catch errors early because requests are validated against the schema.

---

### 3. **Avoids Over-Fetching and Under-Fetching**

- **Over-fetching (REST issue):**When an API returns more data than needed. Example: Fetching `/users` might return a full profile (name, email, address, posts) when you only need the name.
- **Under-fetching (REST issue):**When an API returns less data than needed, requiring multiple requests. Example: To get a user’s name and their 5 latest posts, you might have to call `/users/{id}` and `/users/{id}/posts`.
- **GraphQL Solution:**

  - Clients specify **exactly what data they need** in the query.
  - Example:
    ```graphql
    query {
      user(id: 1) {
        name
        posts(limit: 5) {
          title
        }
      }
    }
    ```
  - The server responds with just the requested fields.
- Benefit:

  - Reduces bandwidth usage.
  - Optimizes performance for mobile and low-bandwidth applications.
  - Improves flexibility for clients without requiring backend changes.


# GraphQL architecture (client, server, schema, resolvers)

---

### 1. **Client**

* The **consumer** of the GraphQL API (e.g., web app, mobile app, or third-party service).
* Sends queries, mutations, or subscriptions to the GraphQL server through a  **single endpoint** .
* Specifies exactly what data it needs, avoiding over/under-fetching.
* Uses GraphQL query language to define requests.

---

### 2. **Server**

* The **GraphQL server** receives the request from the client and processes it.
* It is responsible for:
  * Validating the query against the schema.
  * Passing the query to the appropriate  **resolvers** .
  * Returning the response in JSON format.
* Implemented using frameworks like Apollo Server, GraphQL Yoga, or integrated into backend frameworks.

---

### 3. **Schema**

* The  **backbone of GraphQL** .
* Written in GraphQL Schema Definition Language (SDL).
* Defines:
  * **Types** : Objects, scalars, enums, etc.
  * **Queries** : For reading data.
  * **Mutations** : For modifying data.
  * **Subscriptions** : For real-time updates.
* Example:
  ```graphql
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    user(id: ID!): User
    allUsers: [User]
  }
  ```
* Acts as a **contract** between client and server, ensuring both sides agree on available data and operations.

---

### 4. **Resolvers**

* Functions that **fetch the actual data** for each field in the schema.
* The server maps queries to resolvers to fulfill client requests.
* Example:
  ```javascript
  const resolvers = {
    Query: {
      user: (_, { id }) => getUserById(id),
      allUsers: () => getAllUsers()
    }
  }
  ```
* Resolvers can fetch data from:
  * Databases (SQL/NoSQL)
  * REST APIs
  * External services
  * In-memory data

---

### Putting It Together

1. The **client** sends a query:
   ```graphql
   {
     user(id: 1) {
       name
       email
     }
   }
   ```
2. The **server** validates it against the  **schema** .
3. The server calls the corresponding **resolvers** to get data (e.g., from a database).
4. The **response** is sent back as JSON:
   ```json
   {
     "data": {
       "user": {
         "name": "Ahmad",
         "email": "ahmad@example.com"
       }
     }
   }
   ```
