# Finance Data Processing and Access Control Backend

Backend system built using FastAPI for managing users, financial records, and dashboard analytics with role-based access control.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Setup
1. Create venv  
2. Activate venv  
3. Install requirements  
4. Run server  

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload