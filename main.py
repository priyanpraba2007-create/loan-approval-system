from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all websites to talk to your API
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to connect to DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "System Online", "db_status": "Connected"}

@app.post("/apply-loan")
def apply_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # 1. THE FRAUD LOGIC
    # Rule: If Loan is > 10x Income, it's High Risk
    risk_score = 0
    if loan.loan_amount > (loan.income * 10):
        risk_score = 95
        status = "Flagged: High Risk"
    else:
        risk_score = 10
        status = "Approved"

    # 2. SAVE TO POSTGRESQL
    new_entry = models.LoanApplication(
        applicant_name=loan.applicant_name,
        income=loan.income,
        loan_amount=loan.loan_amount,
        risk_score=risk_score,
        status=status
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return {"id": new_entry.id, "final_decision": status, "score": risk_score}