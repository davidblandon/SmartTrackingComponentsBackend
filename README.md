# 🧠 Smart Component Tracking

**Smart Component Tracking** (Backend part) is an API developed with **FastAPI** for managing and tracking components using QR codes.  
It handles QR code generation, reading, and storage for each tracked component in a MongoDB database, providing an efficient and modern solution for asset or component management.

---

## 📚 Table of Contents
- [🛠️ Installation & Execution](#️-installation--execution)  
- [🗂️ Project Structure](#️-project-structure)
- [🌍 Environment Variables](#-environment-variables)  
- [🗄️ Running MongoDB Locally with Docker](#️-running-mongodb-locally-with-docker)    
- [💻 Useful Commands](#-useful-commands)  
- [📘 API Documentation](#-api-documentation)  
- [👥 Credits](#-credits)

---

## 🛠️ Installation & Execution

### 1️⃣ Clone the repository
```bash
git clone https://github.com/davidblandon/SmartTrackingComponentsBackend.git
```

### 2️⃣ Create and activate a virtual environment

#### 🪟 Windows
```bash
cd ..
python -m venv venv
venv\Scripts\activate
```

#### 🐧 macOS / Linux
```bash
cd ..
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

Or install manually if you don’t have the file yet:
```bash
pip install fastapi uvicorn pymongo python-dotenv qrcode[pil] pillow pyzbar dnspython
```

### 4️⃣ Create the `.env` and `.gitignore` files

#### 🧾 .env file
Create a `.env` file in the project root with the following content:

```env
MONGO_URI=your_mongo_atlas_uri
MONGO_DB=your_mongo_atlas_database 
```

> Ask the developer responsible for the database for the correct URI and database.

⚠️ **Important:** Do not share this file publicly!

#### 🧱 .gitignore file
Create a `.gitignore` file at the same level as `.env` and paste this content:

```
venv/
certs/
__pycache__/
controllers/__pycache__/
models/__pycache__/    
database/__pycache__/
schemas/__pycache__/
utils/__pycache__/
*.py[cod]
ENV/
.idea/
.vscode/
*.log
```
### 5️⃣ Run the server

#### Development mode (HTTP)
```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem

```

Open your browser at:  
👉 [http://localhost:8000](http://localhost:8000)

#### API Documentation
- **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)  
- **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🗂️ Project Structure

### 🏛️ Architecture
```
smart_component_tracking/
├── app/
│   ├── main.py                 # Initializes the FastAPI app and registers routes
│   ├── certs/                  # Certs for https
│   ├── routes/                 # Endpoints organized by resource
│   ├── controllers/            # Business logic for each entity
│   ├── models/                 # Data representation classes
│   ├── database/               # MongoDB connection and collection definitions
│   └── utils/                  # Utility functions (QR, validators, helpers)
├── .env                        # Environment variables (not committed)
├── requirements.txt            # Project dependencies
└── README.md
```

---

### 📜 File and Folder Naming Conventions

- **Folders** → `snake_case`  
  ✅ Example: `controllers/`, `models/`, `utils/`  
- **Files** → `snake_case`  
  ✅ Example: `qr_controller.py`, `component_model.py`

---

### 🐍 Code Naming Conventions

| Type | Convention | Example |
|------|-------------|----------|
| Classes | `CamelCase` | `QrService`, `Component`, `MongoConnector` |
| Functions / variables | `snake_case` | `create_qr()`, `read_qr_image()` |
| Constants | `UPPER_CASE_WITH_UNDERSCORES` | `MONGO_URI`, `DEFAULT_QR_SIZE` |
| FastAPI instances | always `app`, `router` | `app = FastAPI()` |

---

### 🔗 Endpoint Conventions

Routes use **singular names** to represent collections:  
✅ `/component`, `/qr`, `/tracking`

Specific resources use their ID in the URL:  
✅ `GET /component/{component_id}`

Custom actions are added clearly:  
✅ `GET /qr/all`, `POST /qr/create`, `POST /qr/read`

---
## 🥭 Running MongoDB Locally with Docker
To avoid SSL, firewall, or external network issues, you can run a local MongoDB instance using Docker.
This is the recommended setup for development.

### 1️⃣ Requirements

- **Docker Desktop (Windows/macOS)**
- **Docker Engine (Linux)**

Verify installation:

```bash
docker --version
```

### 2️⃣ Create a docker-compose.yml file

Place this file at the root of the project:

```bash
services:
  mongo:
    image: mongo:6.0
    container_name: sct_mongo
    restart: unless-stopped
    ports:
      - "27017:27017"      
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongo_data:/data/db  
volumes:
  mongo_data:
```

This will:

✔ Start MongoDB locally
✔ Expose port 27017
✔ Use username/password → root / root
✔ Persist data inside mongo_data/

### 3️⃣ Start MongoDB

```bash
docker compose up -d
```

Check status:
```bash
docker ps
```

You should see:
```bash
sct_mongo   mongo:6   Up   0.0.0.0:27017->27017/tcp
```

### 4️⃣ Configure your .env to use local MongoDB

In the .env you should have:

```bash
MONGO_URI=mongodb://root:root@localhost:27017/
```

and in the database folder, in database:

```bash
MONGO_DB=smart_component_tracking
```
Your FastAPI backend will now connect to your local Mongo container.


## 💻 Useful Commands

### 🔄 Pull latest changes from repo:
```bash
git pull origin main
```

### 📤 Push changes:
```bash
git add .
git commit -m "Describe the changes"
git push origin main
```

### 📦 Update `requirements.txt` after installing a dependency:
```bash
pip freeze > requirements.txt
```

---

## 📘 API Documentation

FastAPI automatically generates documentation endpoints:

- **Swagger UI** → http://localhost:8000/docs  
- **ReDoc** → http://localhost:8000/redoc  

These allow you to test and explore all API routes interactively.

---

## 👥 Credits

Developed for **AURORA Racing** ©  
Built with ❤️ using **FastAPI**, **MongoDB**, and **Python**.
