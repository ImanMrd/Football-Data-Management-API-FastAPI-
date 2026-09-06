# âš½ Football Data Management API

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

A high-performance RESTful API built with Python (FastAPI) and SQLModel to manage relational data for football teams, players, and transfer history. Designed with microservice architecture principles for future cloud deployment.

## ðŸŒŸ Key Features

- **Robust Data Modeling:** Relational database schema built with SQLModel representing Teams, Players, and Player History.
- **Secure Authentication:** Implements JWT (JSON Web Token) authentication (HS256) with secure password hashing using bcrypt.
- **Role-Based Access Control (RBAC):** Distinct dmin and asic user roles to control access to sensitive endpoints.
- **Cloud-Ready:** Lightweight and easily containerizable for deployment to AWS (EC2/ECS) or Kubernetes.

## ðŸ—‚ï¸ Project Structure

`	ext
ðŸ“¦ Football-Data-Management-API-FastAPI-
 â”£ ðŸ“œ auth.py        # JWT configuration, password hashing, and RBAC logic
 â”£ ðŸ“œ main.py        # Database engine setup, data models, and API routing
 â”— ðŸ“œ README.md      # Project documentation
`

## ðŸ› ï¸ Tech Stack

- **Framework:** FastAPI
- **ORM & Database:** SQLModel, SQLite
- **Security:** Passlib (bcrypt), python-jose (JWT)

## ðŸš€ Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
   `ash
   git clone https://github.com/ImanMrd/Football-Data-Management-API-FastAPI-.git
   cd Football-Data-Management-API-FastAPI-
   `

2. **Install dependencies:**
   `ash
   pip install fastapi uvicorn sqlmodel passlib[bcrypt] python-jose[cryptography]
   `

3. **Run the API server:**
   `ash
   uvicorn main:app --reload
   `

4. **Access the API Docs:**
   Navigate to http://127.0.0.1:8000/docs in your browser to interact with the auto-generated Swagger UI.
