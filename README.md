# Real-Time Collaborative Code Editor

A real-time collaborative code editor built using **FastAPI**, **WebSockets**, **Redis (as cache)**, **PostgreSQL**, and **React + Redux**.

Users can:
- Create or join rooms  
- Edit code collaboratively  
- See changes instantly  


# 🚀 Features

- 🔄 Real-time WebSocket-based collaboration  
- 🧠 AI autocomplete (mocked rule-based server logic)  
- ⚡ Redis-backed room cache  
- 🗄️ PostgreSQL persistence  
- 🔐 Clean backend architecture (routers/services/db/models)  
- 🧱 Frontend with Redux  
- ⚙️ REST + WebSockets working together

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 🧩 Components

### 1. Frontend: React + Redux
- **Responsibilities:**
  - Render code editor (Monaco/CodeMirror)
  - Manage editor state via Redux
  - Connect to WebSocket for real-time updates
  - Call REST endpoints for room creation or fallback updates

- **Why Redux?**  
  Ensures local and remote state stays in sync and avoids unnecessary REST calls for frequent changes.


### 2. Backend: FastAPI (REST + WebSockets)
- **REST Endpoints:**
  - Create/join room
  - Fetch room data
  - Fallback code updates
  - Mock AI autocomplete

- **WebSockets:**
  - Handles real-time code sync between users
  - Sends updates to all participants in a room instantly

- **Why FastAPI?**
  - Asynchronous by design (great for WebSockets)
  - Clean routing and dependency injection
  - Easy to extend with services for database/cache


### 3. Redis (Cache for Active Rooms)
- **Purpose:**
  - Store the current state of each room (code, language, timestamps)
  - Fast retrieval of active room state for new participants
  - Reduce load on PostgreSQL

- **Why Redis?**
  - In-memory storage → low latency
  - Perfect for ephemeral data
  - Helps scale WebSocket servers horizontally


### 4. PostgreSQL (Persistent Storage)
- **Purpose:**
  - Store permanent room data
  - Keep code and metadata durable
  - Backup/restore support

- **Why PostgreSQL?**
  - ACID compliance ensures reliable data
  - Handles structured relational data efficiently
  - Works well with caching layer for hybrid real-time + persistent storage


### How It Works Together
1. User joins a room via frontend  
2. Frontend fetches room info via REST (or creates new room)  
3. WebSocket connection opens → code updates are sent/received in real-time  
4. Redis cache stores active room state for fast access  
5. PostgreSQL stores persistent data for durability  

This architecture ensures:
- Low-latency collaboration  
- Persistent code storage  
- Clean separation of concerns between frontend, backend, cache, and database


# Data Flow Diagram

<img width="1536" height="1024" alt="ChatGPT Image Dec 2, 2025, 01_39_54 AM" src="https://github.com/user-attachments/assets/65cba5c1-91f6-471a-b8ba-5b098c696e58" />


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# 🏃‍♂️ Running the Real-Time Collaborative Code Editor

This guide will help you set up and run the full application locally, including **PostgreSQL**, **Redis**, **FastAPI backend**, and **React frontend**.

---

## 1️⃣ Prerequisites

- Docker & Docker Compose installed  
- Python 3.11+  
- Node.js & npm  

---

## 2️⃣ Start PostgreSQL and Redis using Docker Compose

Find `docker-compose.yml` in your backend folder and then run `docker-compose up -d`

---

## 1️⃣ Backend Setup (FastAPI)

### 1.1 Create and activate a virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows
```

### 1.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 1.3 Run the FastAPI Backend

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 2️⃣ Frontend Setup (React + TypeScript + Redux)

### 2.1 Go to the frontend folder

```bash
cd frontend
```

### 2.2 Install dependencies

```bash
npm install
```

### 2.3 Start the development server

```bash
npm run dev
```

---

Frontend app will run at: http://localhost:5173
