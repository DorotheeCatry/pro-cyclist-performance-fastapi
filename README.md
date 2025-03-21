
# 🚴 Pro Cyclist Performance API  

## 📌 Description  
The **Pro Cyclist Performance API** is a FastAPI-based project designed to manage professional cyclists' performance data. It provides secure authentication, athlete performance tracking, and advanced statistics.  

---

## 👥 Authors 
**Dorothée Catry** : `https://github.com/DorotheeCatry/` 

**Samuel Thorez-Debrucq** : `https://github.com/SamuelTD/`


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
│-- .venv/                                    # Virtual environment
│-- app/                                      # Application code
│   │-- api/                                  # API routes
│   │   │-- v1/                               # API versioning
│   │       │-- endpoints/                    # Endpoints
│   │           │-- auth.py                   # Authentication routes
│   │           │-- stats.py                  # Statistics-related routes
│   │           │-- users.py                  # User-related routes
│   │-- core/                                 # Core configurations
│   │   │-- config.py                         # Configuration settings
│   │   │-- security.py                       # Security utilities
│   │-- db/                                   # Database logic
│   │   │-- athlete.py                        # Athlete model management
│   │   │-- db_utils.py                       # Database utility functions
│   │   │-- selects.py                        # Query functions
│   │   │-- test_session.py                   # Database test session
│   │   │-- users.db                          # SQLite database file
│   │-- utils/                                # Utility functions
│   │-- main.py                               # FastAPI entry point
│-- streamlit_app/                            # Streamlit application folder
│   │-- images/                               # Images folder
│   │-- enums.py                              # Enum definitions
│   │-- main.py                               # Main Streamlit entry point
│   │-- streamlit_functions.py                # Streamlit utility functions
│-- .env                                      # Environment variables
│-- .gitignore                                # Git ignored files
│-- LICENSE                                   # License file
│-- README.md                                 # Project documentation
│-- requirements.txt                          # Dependencies

```

---

## 🔑 Authentication & Security  
- **Password hashing** with bcrypt.  
- **JWT authentication** using OAuth2.  
- **User management** (registration, login, session security).  

---

## 📌 API Endpoints  
| Method   | URL                                | Description                                                            | Access        |
|----------|------------------------------------|------------------------------------------------------------------------|---------------|
| **POST** | `/auth/register`                   | Register a new user                                                    | Public        |
| **POST** | `/auth/login`                      | Authenticate & get a JWT token                                         | Public        |
| **POST** | `/users/modify_athlete`            | Modify an athlete's details                                            | Authenticated |
| **POST** | `/users/create_session`            | Create a new training session                                          | Authenticated |
| **POST** | `/users/get_athlete`               | Get athlete details by ID                                              | Authenticated |
| **GET**  | `/users/get_sessions`              | Get sessions for the current athlete                                   | Authenticated |
| **GET**  | `/users/get_sessions_coach`        | Get sessions for a specified athlete (for coaches)                     | Authenticated |
| **GET**  | `/users/get_athlete_list`          | Get a list of athletes                                                 | Authenticated |
| **GET**  | `/users/delete_account`            | Delete a user account                                                  | Authenticated |
| **GET**  | `/stats/get_most_powerful`         | Get the most powerful athlete                                          | Authenticated |
| **GET**  | `/stats/get_best_VO2max`           | Get the athlete with the best VO2max                                   | Authenticated |
| **GET**  | `/stats/get_best_power_to_weight`  | Get the athlete with the best power-to-weight ratio                    | Authenticated |


---

## 🚀 Installation & Deployment  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/DorotheeCatry/pro-cyclist-performance-api.git
cd pro-cyclist-performance-api
```

### 2️⃣ Create your environment  

Linux : 
```bash
 python -m venv .venv  
 source .venv/bin/activate
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Create your .env file 

Create a .env file in the root directory. This file should contain the following environment variables : 

SECRET_KEY -> A string sequence used in the encryption of the API's token system. We recommend using the following for generation : 
```bash
import secrets

secret_key = secrets.token_hex(32)  # Generates a 64-character hex string (32 bytes)
print(secret_key)
```

API_URL -> The base URL of your API. By default it should be : ̀"http://127.0.0.1:8086/api/v1/"

### 5️⃣ Start the API  
```bash
uvicorn app.main:app --port 8086 --reload
```
The API will be available at `http://127.0.0.1:8086` 🚀.

### 6️⃣ Start the Streamlit app 
```bash
streamlit run streamlit_app/main.py 
```
This will automatically open a web browser page at `http://127.0.0.1:8080` with your streamlit app 🚀.

---

## Database structure 

Here's a link to the CDM, LDM and PDM of the project : 
https://lucid.app/lucidchart/62f97da6-da57-4409-8f78-136eb1b7e388/edit?viewport_loc=-1223%2C-663%2C2216%2C1093%2CHWEp-vi-RSFO&invitationId=inv_1618ede1-fefe-4399-b1dd-923b894550e1

---

## 📜 License  
This project is open-source and available under the **MIT License**.  

🚴‍♂️ _Analyze and track professional cyclists' performance with FastAPI!_ 🚀
