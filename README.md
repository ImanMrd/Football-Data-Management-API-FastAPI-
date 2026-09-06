# ⚽ Football Data Management API

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

A high-performance RESTful API built with Python (FastAPI) and SQLModel to manage relational data for football teams, players, and transfer history. Designed with microservice architecture principles for future cloud deployment.

## 🌟 Key Features

- **Robust Data Modeling:** Relational database schema built with SQLModel representing Teams, Players, and Player History.
- **Secure Authentication:** Implements JWT (JSON Web Token) authentication (HS256) with secure password hashing using bcrypt.
- **Role-Based Access Control (RBAC):** Distinct `admin` and `basic` user roles to control access to sensitive endpoints.
- **Cloud-Ready:** Lightweight and easily containerizable for deployment to AWS (EC2/ECS) or Kubernetes.

## 🗂️ Project Structure

```text
📦 Football-Data-Management-API-FastAPI-
 ┣ 📜 auth.py        # JWT configuration, password hashing, and RBAC logic
 ┣ 📜 main.py        # Database engine setup, data models, and API routing
 ┗ 📜 README.md      # Project documentation
```

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **ORM & Database:** SQLModel, SQLite
- **Security:** Passlib (bcrypt), python-jose (JWT)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ImanMrd/Football-Data-Management-API-FastAPI-.git
   cd Football-Data-Management-API-FastAPI-
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlmodel passlib[bcrypt] python-jose[cryptography]
   ```

3. **Run the API server:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API Docs:**
   Navigate to `http://127.0.0.1:8000/docs` in your browser to interact with the auto-generated Swagger UI.
