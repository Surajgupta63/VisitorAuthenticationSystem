# Visitor Management System (VMS)

## Overview
The **Visitor Management System (VMS)** is a web application built using Flask that allows organizations to manage visitor entries, including details like name, mobile number, purpose of visit, and check-in/check-out times. The system also implements authentication using JWT tokens for secure access control.

## Features
- **User Authentication** (Register, Login, Logout)
- **Token-based Authentication** using JWT
- **Multiple Database Support** (User and Visitor data stored separately)
- **CRUD Operations** for managing visitor records
- **Photo Upload & Storage**
- **Private Routing for Secure Access**
- **Responsive UI with Bootstrap**

## Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: SQLite
- **Frontend**: HTML, Bootstrap
- **Security**: bcrypt (for password hashing), JWT (for authentication)

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/vms.git
cd vms
```

### 2. Create a Virtual Environment
#### Windows:
```sh
python -m venv venv
venv\Scripts\activate
```
#### macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up the Database
```sh
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 5. Run the Application
```sh
python app.py
```

The app will start running on `http://127.0.0.1:8000/`

---

## API Endpoints

### **Authentication Routes**
| Endpoint        | Method | Description |
|---------------|--------|-------------|
| `/register`   | POST   | Register a new user |
| `/login`      | POST   | Login and receive a JWT token |
| `/logout`     | GET    | Logout user (clears session) |

### **Visitor Management Routes**
| Endpoint       | Method | Description |
|--------------|--------|-------------|
| `/`          | GET    | Home page (Redirects to login) |
| `/dashboard` | GET    | View visitor records (Requires authentication) |
| `/photo`     | GET    | Photo upload page |
| `/upload`    | POST   | Upload visitor image |
| `/update/<sno>` | POST | Update visitor details |
| `/delete/<sno>` | GET  | Delete visitor record |

---

## Private Routing
- The dashboard and visitor management pages are **only accessible if the user is logged in**.
- If the user tries to access `127.0.0.1:8000/dashboard` without logging in, they are redirected to `/login`.
- JWT Token is stored in the browser's **local storage** for authentication.

---

## Screenshots
> (Add relevant screenshots of your app UI here)

---

## License
This project is licensed under the **MIT License**.

---

## Author
Developed by **Suraj Gupta**.

[LinkedIn](https://www.linkedin.com/in/guptasurajlpu/) | [GitHub](https://github.com/Surajgupta63/)

