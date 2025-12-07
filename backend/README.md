# Layer Flow Backend

Backend for layer-flow (FastAPI + PostGIS)

## Prerequisites

- Python 3.x
- PostgreSQL with PostGIS extension

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   Copy `.env.example` to `.env` and update the values.
   Set `DATABASE_URL` to your PostgreSQL connection string.

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
