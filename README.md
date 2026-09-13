# 📝 Blog API

A production-ready RESTful Blog API built with **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**.

This project provides a robust backend system for managing blog posts, comments, categories, and user profiles. It includes essential production features like pagination, advanced filtering, full-text searching, dynamic sorting, IP-based rate limiting, and strict input validation/sanitization.

The API is fully documented and interactive out-of-the-box through **Swagger UI / OpenAPI**.

---

## 📌 Project Overview

The **Blog API** is designed to handle all core functionalities required for a modern blogging platform. It ensures high reliability and security by implementing data validation pipelines and protecting endpoints from abuse.

### Key Features
* **Full CRUD Management:** Complete control over Users, Categories, Posts, and Comments.
* **Robust Data Layer:** Powered by PostgreSQL and SQLAlchemy ORM.
* **Advanced Querying:** Native support for Pagination (with metadata), Filtering, Searching, and Sorting.
* **Security & Optimization:** IP-based Rate Limiting, strict Input Validation, and automatic Data Sanitization (stripping whitespaces).
* **API Documentation:** Interactive documentation powered by Swagger/OpenAPI.
* **Standardized Responses:** Proper HTTP status codes and detailed validation error messages.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Primary programming language |
| **FastAPI** | High-performance backend REST framework |
| **PostgreSQL** | Relational database management system |
| **SQLAlchemy** | Object-Relational Mapping (ORM) and DB queries |
| **Pydantic** | Strict data validation, serialization, and schemas |
| **Uvicorn** | High-speed ASGI web server |
| **Swagger/OpenAPI** | Automated API interactive testing & documentation |
| **Git / GitHub** | Version control and source code repository |
| **Docker** | Containerization and deployment engine |

---

## 🏗️ Project Architecture

The project follows a clean, modular structure separating routers, data models, validation schemas, and core configuration.

```text
blog-api/
│
├── app/
│   ├── routers/
│   │   ├── users.py
│   │   ├── categories.py
│   │   ├── posts.py
│   │   └── comments.py
│   │
│   ├── database.py       # DB connection & SQLAlchemy config
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic validation & HTML/String sanitization
│   ├── rate_limiter.py   # IP-based rate limiting middleware
│   └── main.py           # FastAPI application entrypoint
│
├── .env                  # Environment variables (DB credentials, etc.)
├── .gitignore            # Git ignore configuration
├── DOCKERFILE            # Containerization configuration
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

### File & Folder Responsibilities
* **`app/main.py`:** Initializes the FastAPI instance, manages CORS/middlewares, and mounts all component routers.
* **`app/database.py`:** Initializes the database engine, creates sessions, and provides the DB dependency injection context.
* **`app/models.py`:** Defines the database architecture, schema constraints, and foreign key relationships.
* **`app/schemas.py`:** Manages incoming request validation (`In` schemas), outgoing response serialization (`Out` schemas), and data cleanup.
* **`app/routers/`:** Contains isolated API modules. Each file manages endpoints for its respective domain entity.
* **`app/rate_limiter.py`:** Tracks incoming request timestamps against client IPs to throttle abusive clients.

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites
Make sure you have the following installed on your machine:
* Python (v3.9 or higher)
* PostgreSQL Database Server
* Git

### 1. Clone the Repository
```bash
git clone https://github.com
cd blog-api
```

### 2. Create a Virtual Environment
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of the project and add your database configuration:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/blog_db
```

### 5. Run the Application
Start the Uvicorn local development server:
```bash
uvicorn app.main:app --reload
```
The server will start running at `http://127.0.0.1:8000`.

---

## 🐳 Docker Deployment

If you prefer running the application inside a isolated container environment, you can use Docker.

### Build the Docker Image
```bash
docker build -t blog-api .
```

### Run the Docker Container
```bash
docker run -d --name blog-api-container -p 8000:8000 --env-file .env blog-api
```

---

## 🗄️ Database Design & Relationships

The relational database structure consists of 4 main entities mapped using **SQLAlchemy ORM**.

### Table Schemas
* **`users`:** `id` (PK), `name`, `email` (Unique), `password` (Hashed)
* **`categories`:** `id` (PK), `name` (Unique)
* **`posts`:** `id` (PK), `title`, `content`, `author_id` (FK), `category_id` (FK), `created_at`, `updated_at`
* **`comments`:** `id` (PK), `content`, `post_id` (FK), `author_id` (FK), `created_at`, `updated_at`

### Relationships Mapping
* A **User** can write multiple posts and write multiple comments.
* A **Category** can group multiple blog posts.
* A **Post** can contain multiple comments, but belongs to exactly one *Author* and one *Category*.
* A **Comment** is linked exclusively to one *Post* and one *User*.

---

## 📡 API Endpoints Reference

### 👤 Users Management

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users/` | Register a new user |
| `GET` | `/users/` | Retrieve all registered users |
| `GET` | `/users/{id}` | Fetch specific user profile by ID |
| `PUT` | `/users/{id}` | Update existing user details |
| `DELETE` | `/users/{id}` | Delete user account |

### 📂 Categories

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/categories/` | Create a new blog category |
| `GET` | `/categories/` | List all available categories |
| `GET` | `/categories/{id}` | Fetch category details by ID |
| `PUT` | `/categories/{id}` | Update a category name |
| `DELETE` | `/categories/{id}` | Remove a category |

### 📝 Blog Posts

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/posts/` | Publish a new blog post |
| `GET` | `/posts/` | Fetch posts with pagination, filtering, and search |
| `GET` | `/posts/{id}` | Retrieve a full post by its ID |
| `PUT` | `/posts/{id}` | Edit an existing post |
| `DELETE` | `/posts/{id}` | Delete a post |

* **Example Payload (`POST /posts/`):**
```json
{
  "title": "Introduction to FastAPI",
  "content": "FastAPI is a modern Python web framework.",
  "author_id": 1,
  "category_id": 1
}
```

### 💬 Comments

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/comments/` | Add a comment to a specific post |
| `GET` | `/comments/` | Fetch all comments across the platform |
| `GET` | `/comments/{id}` | Get a specific comment by ID |
| `PUT` | `/comments/{id}` | Edit comment content |
| `DELETE` | `/comments/{id}` | Remove a comment |

---

## ⚡ Querying, Performance & Security

### 📄 Pagination
To optimize payload delivery, the `GET /posts/` endpoint paginates large collections.
* **Query Parameters:** `page` (default: 1), `limit` (default: 10)
* **Request Example:** `GET /posts/?page=2&limit=10`
* **Internal Logic:** The database offset is dynamically calculated as:
  \[\text{offset} = (\text{page} - 1) \times \text{limit}\]
  *(e.g., Page 2 skips the first 10 records and reads from the 11th).*

#### Pagination Metadata Output
```json
{
  "page": 2,
  "limit": 10,
  "total": 25,
  "pages": 3,
  "items": [ ... ]
}
```

### 🔎 Filtering & Full-Text Search
You can narrow down results by chaining multiple independent query filters:
* **Filter by Author:** `GET /posts/?author_id=1`
* **Filter by Category:** `GET /posts/?category_id=3`
* **Case-Insensitive Search:** `GET /posts/?search=fastapi` (Searches both the `title` and `content` fields dynamically matching variations like *FastAPI*, *FASTAPI*, or *fastapi*).
* **Combined Query:** `GET /posts/?author_id=1&category_id=1&search=FastAPI`

### ↕️ Dynamic Sorting
Posts can be ordered dynamically based on strict pre-validated database attributes:
* **Allowed Fields:** `title`, `created_at`, `updated_at`
* **Allowed Order:** `asc` (Ascending) or `desc` (Descending)
* **Example:** `GET /posts/?sort=created_at&order=desc`

---

## 🛡️ Security Features

### IP-Based Rate Limiting
To prevent API abuse and DoS attacks, the backend enforces request limits.
* **Current Threshold:** **10 requests per 60 seconds** per unique client IP address.
* **Violation Response:** If exceeded, an `HTTP 429 Too Many Requests` is thrown immediately.

```text
Client Request ──► [ Rate Limiter Check ] ──┬─► Allowed (Within Limit) ──► Execute Route
                                            └─► Exceeded ───────────────► HTTP 429 Error
```

> 💡 *Note: The current tracking logic utilizes an in-memory window mechanism ideal for small scales. For heavy-traffic distributed architectures, swapping out the memory driver for a shared **Redis server** setup is highly recommended.*

### 🧹 Input Validation & Sanitization
All incoming string data payloads undergo runtime cleaning and schema validation through **Pydantic**:
* String attributes automatically strip unwanted leading and trailing whitespaces.
* Incoming malicious inputs or mismatched types are caught before running database statements, returning a structured `422 Unprocessable Entity` JSON error payload.

**Example Input Sanitization Flow:**
```json
// Incoming Raw Request Body
{
  "title": "   My First Blog   ",
  "content": "   Hello FastAPI   "
}

// Internal Sanitized State before saving
{
  "title": "My First Blog",
  "content": "Hello FastAPI"
}
```

---

## 📖 API Documentation & Testing

FastAPI automatically generates interactive documentations. Once your server is running, you can explore and test the endpoints directly from your browser:

* **Interactive Swagger UI:** `http://127.0.0` (Allows executing direct sample HTTP requests).
* **Alternative ReDoc UI:** `http://127.0.0` (Clean, organized API blueprint viewing).
