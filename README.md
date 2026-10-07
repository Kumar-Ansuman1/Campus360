# Campus360 — EcoFacility AI

Campus360 is an AI-powered smart-facility intelligence platform for monitoring and understanding campus operations.

It combines a FastAPI backend, an AI intelligence pipeline, and a React-based dashboard to turn facility telemetry into operational KPIs, anomaly status, forecasts, recommendations, what-if analysis, and Digital Twin visualization data.

## Overview

The platform follows this flow:

```text
Campus / Facility Data
        │
        ▼
   FastAPI Backend
        │
        ▼
  Campus360 AI Pipeline
        │
        ├── Data normalization
        ├── Anomaly detection
        ├── KPI extraction
        ├── Forecasting
        ├── Semantic RAG
        ├── Decision reasoning
        ├── Recommendations
        ├── What-If simulation
        ├── Current-status analysis
        └── Digital Twin state
        │
        ▼
   React Dashboard
```

The dashboard consumes the unified AI response from:

```text
GET /api/ai/dashboard
```

---

## Key Capabilities

### Facility Intelligence
- Facility and building information
- Energy monitoring
- Water monitoring
- Waste monitoring
- Traffic and vehicle monitoring
- Parking utilization
- Average speed

### AI Intelligence
- Operational anomaly detection
- KPI extraction
- Forecasting
- Semantic RAG/context retrieval
- Decision reasoning
- AI-generated explanations
- Priority and confidence assessment
- Recommendations
- What-If energy simulations

### Digital Twin
The AI pipeline generates a Digital Twin-ready state containing:
- Building information
- Current operational status
- Energy
- Water
- Waste
- Vehicles
- Parking
- Average speed
- Forecast trend
- Priority
- What-If information
- Visualization states

The React dashboard presents this state interactively.

---

# Technology Stack

## Backend

- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- NumPy
- Pandas
- pytest

## AI Layer

- Python
- Anomaly detection
- Forecasting
- Semantic RAG
- Decision reasoning
- Recommendation engine
- What-If simulation

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Recharts
- Three.js
- React Three Fiber
- Drei

---

# Project Structure

```text
Campus360/
│
├── ai/
│   ├── data_loader.py
│   └── intelligence/
│       ├── anomaly.py
│       ├── forecasting.py
│       ├── pipeline.py
│       ├── reasoning.py
│       ├── recommendations.py
│       ├── what_if.py
│       └── ...
│
├── backend/
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── integrations/
│   ├── storage/
│   │   └── ecofacility.db
│   ├── tests/
│   └── utils/
│
├── dashboard/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   └── dashboard/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── migrations/
├── models/
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

# Backend Setup

## Prerequisites

Install:

- Python 3.12+
- pip
- Node.js and npm

Verify:

```powershell
python --version
pip --version
node --version
npm --version
```

## Create a Python Environment

From the project root:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

## Environment

The example configuration is available in:

```text
.env.example
```

Do not commit a real `.env` file containing secrets.

## Database

The development database is:

```text
backend/storage/ecofacility.db
```

The repository includes the development SQLite database used by the current hackathon setup.

For migration management:

```powershell
alembic check
alembic upgrade head
```

---

# Run the Backend

From the project root:

```powershell
uvicorn backend.main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### Health Check

```text
GET /health
GET /health/database
```

### Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

---

# AI API

The AI routes are under:

```text
/api/ai
```

### AI Health

```text
GET /api/ai/health
```

### Dashboard Intelligence

```text
GET /api/ai/dashboard
```

This is the primary endpoint consumed by the React dashboard.

It provides structured data for:

- Facility
- Building
- KPIs
- Anomalies
- Current status
- Forecast
- Explanation
- Recommendation
- RAG output
- Reasoning
- What-If analysis
- Digital Twin state

### Run AI Pipeline

```text
POST /api/ai/run
```

---

# Frontend Setup

Open a second terminal and enter the dashboard:

```powershell
cd dashboard
```

Install dependencies:

```powershell
npm install
```

Run the development server:

```powershell
npm run dev
```

The Vite development server normally runs at:

```text
http://localhost:5173
```

The dashboard currently consumes the backend at:

```text
http://127.0.0.1:8000
```

The API integration is implemented in:

```text
dashboard/src/api/dashboardApi.ts
```

---

# Frontend Dashboard

The dashboard is organized as a responsive bento/grid interface containing:

1. Facility Header
2. KPI Cards
3. Forecast
4. Facility Alerts
5. AI Insight
6. Digital Twin
7. AI Recommendations
8. What-If Analysis

The dashboard is designed to consume backend-generated values rather than hard-coded operational data.

---

# Build the Frontend

To create a production build:

```powershell
cd dashboard
npm run build
```

Preview the production build:

```powershell
npm run preview
```

---

# AI Pipeline

The unified intelligence pipeline follows:

```text
Backend Telemetry
        ↓
Data Normalization
        ↓
Anomaly Detection
        ↓
KPI Extraction
        ↓
Forecasting
        ↓
Advanced Semantic RAG
        ↓
Decision Reasoning
        ↓
Recommendations
        ↓
What-If Simulation
        ↓
Current Status Analysis
        ↓
What-If Impact Analysis
        ↓
Digital Twin Visualization Data
```

The main orchestration code is:

```text
ai/intelligence/pipeline.py
```

The pipeline produces a machine-readable dashboard response that is exposed through the FastAPI AI router.

---

# Dashboard Data Contract

The frontend consumes the unified response returned by:

```text
GET /api/ai/dashboard
```

Important data groups include:

```text
facility
building
kpis
anomalies
current_status
forecast
explanation
recommendation
rag
reasoning
recommendation_details
what_if
what_if_analysis
digital_twin
```

The TypeScript contract is maintained in:

```text
dashboard/src/types/dashboard.ts
```

---

# Testing

The backend uses pytest.

Run:

```powershell
pytest -v
```

The backend test suite covers areas including:

- Health
- Facilities
- Buildings
- Devices
- Telemetry
- Energy
- Water
- Waste
- Traffic
- Air Quality
- Assets
- Alerts
- Recommendations

---

# Development Workflow

Recommended workflow:

```text
1. Understand the existing module
          ↓
2. Make the smallest required change
          ↓
3. Run backend/frontend checks
          ↓
4. Test the affected API or UI
          ↓
5. Verify integration
          ↓
6. Commit the change
          ↓
7. Push to GitHub
```

For frontend changes:

```powershell
cd dashboard
npm run build
```

For backend changes:

```powershell
pytest -v
```

When database models change, review and run the appropriate Alembic migration workflow.

---

# Team Responsibilities

## Backend
Responsible for:
- FastAPI REST APIs
- Database
- SQLAlchemy models
- Pydantic schemas
- Services
- Validation
- Exception handling
- Migrations
- API integration contracts

## AI / Analytics
Responsible for:
- Data normalization
- Anomaly detection
- KPI extraction
- Forecasting
- RAG
- Decision reasoning
- Recommendations
- What-If analysis
- Digital Twin-ready intelligence state

## Dashboard / Frontend
Responsible for:
- React dashboard
- KPI visualization
- Forecast visualization
- Alert presentation
- AI insight presentation
- Recommendations
- What-If presentation
- Digital Twin visualization
- Frontend API integration
- Responsive UI

---

# Local Development

The complete local development setup uses two processes.

### Terminal 1 — Backend

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --port 8000
```

### Terminal 2 — Dashboard

```powershell
cd dashboard
npm install
npm run dev
```

Then open the Vite URL shown in the terminal.

---

# Current Status

The current Campus360 implementation includes:

- FastAPI backend
- SQLite persistence
- SQLAlchemy ORM
- Alembic migrations
- REST API modules
- AI intelligence pipeline
- Anomaly detection
- KPI extraction
- Forecasting
- Semantic RAG
- Decision reasoning
- Recommendation engine
- What-If simulation
- Digital Twin state generation
- React + TypeScript dashboard
- Recharts visualizations
- Three.js Digital Twin visualization
- Frontend-to-AI API integration
- Production frontend build

The dashboard has been verified locally with the current AI dashboard response, and the production frontend build completes successfully.

---

# Repository

GitHub:

https://github.com/Kumar-Ansuman1/Campus360
