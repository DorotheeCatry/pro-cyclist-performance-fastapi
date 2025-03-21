Here is the **README** in **English**:  

---

# 🚴 Pro Cyclist Performance API  

## 📌 Description  
The **Pro Cyclist Performance API** is a FastAPI-based project designed to manage professional cyclists' performance data. It provides secure authentication, athlete performance tracking, and advanced statistics.  

---

## 👥 Creators  
**Samuel Thorez-Debrucq** & **Dorothée Catry**  

---

## 🎯 Objectives  
- 🔐 **Secure authentication** with JWT (user registration & login).  
- 🚴 **Athlete management** (add, update, delete).  
- 📊 **Performance tracking** (power, VO2max, weight-to-power ratio).  
- 📈 **Advanced statistics** to identify top-performing athletes.  
- 🖥 **Bonus: Streamlit & Power BI integration** for data visualization.  

---

## 🛠 Technologies  
| **Component** | **Technology** |
|--------------|---------------|
| Language | Python |
| Framework | FastAPI |
| Database | SQLite |
| Security | JWT (OAuth2), bcrypt |
| Visualization | Streamlit, Power BI |

---

## 📂 Project Structure  

```
PRO-CYCLIST-PERFORMANCE-API/
│-- .venv/                   # Virtual environment
│-- app/
│   │-- api/                 # API routes
│   │   │-- v1/              # API versioning
│   │       │-- endpoints/   # Endpoints
│   │           │-- auth.py  # Authentication routes
│   │           │-- stats.py # Statistics-related routes
│   │           │-- users.py # User-related routes
|   |           |-- stats.py # Statistics-related routes
│   │-- core/                # Core configurations
│   │   │-- config.py        # Configuration settings
│   │   │-- security.py      # Security utilities
│   │-- db/                  # Database logic
│   │   │-- athlete.py       # Athlete model management
│   │   │-- db_utils.py      # Database utility functions
│   │   │-- selects.py       # Query functions
│   │   │-- test_session.py  # Database test session
│   │   │-- users.db         # SQLite database file
│   │-- utils/               # Utility functions
│   │-- main.py              # FastAPI entry point
│-- .env                     # Environment variables
│-- .gitignore               # Git ignored files
│-- LICENSE                  # License file
│-- README.md                # Project documentation
│-- requirements.txt         # Dependencies
```

---

## 🔑 Authentication & Security  
- **Password hashing** with bcrypt.  
- **JWT authentication** using OAuth2.  
- **User management** (registration, login, session security).  

---

## 📌 API Endpoints  
| Method | URL | Description | Access |
|--------|-----|------------|--------|
| **POST** | `/auth/register` | Register a new user | Public |
| **POST** | `/auth/login` | Authenticate & get a JWT token | Public |
| **POST**  | `/users/modify_athlete` | Modify an athlete's details | Authenticated |
| **POST** | `/users/create_session` | Create a new training session | Authenticated |
| **GET**  | `/stats/get_most_powerful` | Get the most powerful athlete | Authenticated |
| **GET**  | `/stats/get_best_VO2max` | Get the athlete with the best VO2max | Authenticated |
| **GET**  | `/stats/get_best_power_to_weight` | Get the athlete with the best power-to-weight ratio | Authenticated |

---

## 🚀 Installation & Deployment  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/DorotheeCatry/pro-cyclist-performance-api.git
cd pro-cyclist-performance-api
```

### 2️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Start the API  
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000 🚀`.

---

## ✅ Running Tests  
To run unit tests, use:  
```bash
pytest
```

---

## 📜 License  
This project is open-source and available under the **MIT License**.  

🚴‍♂️ _Analyze and track professional cyclists' performance with FastAPI!_ 🚀