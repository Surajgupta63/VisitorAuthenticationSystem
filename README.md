# Visitor Authentication System (VAS)

## Overview
The **Visitor Authentication System (VAS)** is a web application built using Flask that allows organizations to manage visitor entries, including details like name, mobile number, purpose of visit, vistors live photo capturing and check-in/check-out times. The system also implements authentication for secure access control.

## Features
- **User Authentication** (Register, Login, Logout)
- **Multiple Database Support** (User and Visitor data stored separately)
- **CRUD Operations** for managing visitor records
- **Photo Upload & Storage**
- **Responsive UI with Bootstrap**

## Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: SQLite
- **Frontend**: HTML, Bootstrap
- **Security**: bcrypt (for password hashing)

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

## Authentication
- The dashboard and visitor management pages are **only accessible if the user is logged in**.
- If the user tries to access `127.0.0.1:8000/dashboard` without logging in, they are redirected to `/login`.

---

## Screenshots
> (Screenshots)
> ![snap1](https://github.com/user-attachments/assets/caaa2854-8486-4e05-bf7c-e6261d4d5c25)
> ![snap2](https://github.com/user-attachments/assets/8de18b24-4f55-4f18-a389-5c1b43faae6e)
> ![snap3](https://github.com/user-attachments/assets/a88180e1-7bc0-4cc6-821f-46ba1b4c16a1)
> ![snap4](https://github.com/user-attachments/assets/1b689ba2-a236-441c-8f8d-0edc0fd5fd2b)
> ![snap5](https://github.com/user-attachments/assets/547f8ecb-4c94-4871-a6e4-678384a6dda2)
> ![snap6](https://github.com/user-attachments/assets/ed608fc0-6ce9-4978-97fc-80a99b051b69)
> ![snap7](https://github.com/user-attachments/assets/38e1c88f-6bc1-4f12-b967-e37984ce62d1)


---


## Author
Developed by **Suraj Gupta**.

[LinkedIn](https://www.linkedin.com/in/guptasurajlpu/) | [GitHub](https://github.com/Surajgupta63/)


