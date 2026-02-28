# Hardware Checkout App  
Cloud Native Team Project  

---

## 1. Overview

This application is a full-stack web system for managing:

- User authentication  
- Project creation and ownership  
- Project membership  
- (Planned) Hardware inventory allocation  

The system is built using:

- **Frontend:** React + TypeScript + Vite + Material UI  
- **Backend:** Flask (Python) using app factory pattern  
- **Database:** MongoDB  
- **Containerization:** Docker (MongoDB service)  

The project is under active development. Some hardware endpoints are designed but not yet implemented.

---

## 2. Current Functional Scope (Accurate Status)

| Feature | Status | Notes |
|----------|--------|-------|
| User Registration | Implemented | Custom cyclic cipher encryption |
| User Login | Implemented | 24-hour session persistence (localStorage) |
| Session Management | Implemented | Frontend-managed session |
| Create Project | Implemented | Unique projectId validation |
| List Projects | Implemented | Owner filtering supported |
| Join/Leave Project | Implemented | Via Projects API |
| Delete Project | Implemented | Owner restricted |
| Health Endpoint | Implemented | `/api/health` |
| Hardware Inventory Listing | Not Implemented | — |
| Hardware Checkout | Not Implemented | — |
| Hardware Check-in | Not Implemented | — |
| Approval Workflow | Not Implemented | — |
| Automated Backend Testing | Not Implemented | — |

This table reflects the current repository state.

---

## 3. System Architecture

### Frontend

- React (Vite build system)  
- TypeScript  
- Material UI (MUI)  
- Context-based authentication  
- Axios-based API abstraction layer  
- Protected routes  

Runs locally on:
http://localhost:5173


---

### Backend

- Flask (app factory pattern)  
- Blueprint-based route organization  
- MongoDB via PyMongo  
- Custom cyclic cipher for credential encryption  
- Environment-based configuration  
- Health check endpoint  

Runs locally on:
http://localhost:5001 


---

### Database

MongoDB collections currently used:

- `users`  
- `projects`  
- (Hardware collections planned but not fully implemented)  

MongoDB runs via Docker Compose.

---

## 4. Authentication Design

- Only `userId` and `password` are required.  
- Credentials are encrypted before storage using a cyclic cipher.  

Session persistence:

- Stored in localStorage  
- 24-hour expiration  
- Entire user object stored client-side  

**Security Note:**  
The current implementation does not use JWT refresh tokens or server-managed sessions.

---

## 5. API Status Summary

### Implemented Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users`
- `POST /api/users`
- `GET /api/projects`
- `POST /api/projects`
- `PATCH` project membership endpoints
- `GET /api/health`

### Designed but Not Implemented

- `/api/hardware`
- `/api/hardware/{id}/checkout`
- `/api/hardware/{id}/checkin`
- `/api/hardware/allocations`

See `docs/API_REFERENCE.md` for detailed endpoint specification and status markers.

---

## 6. Running the Project

### 1. Start MongoDB (Docker)

```bash
docker compose up -d

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
flask run --port 5001

### 3. Frontend
cd frontend
npm install
npm run dev

## 7. Testing Status

### Current Testing Approach

- Manual endpoint testing (Postman)
- Manual UI testing
- Linting for frontend and backend

Automated unit tests are not yet implemented.

A formal structural testing plan is being developed separately for academic coursework.

---

## 8. Development Status

The project is currently:

- Functionally stable for user and project management
- Incomplete for hardware inventory allocation
- Under documentation refinement
- Being aligned with formal software testing methodology

---

## 9. Academic Context

This project is being used for:

- Cloud Native Application Development
- Software Testing (structural testing techniques will be applied to backend logic)