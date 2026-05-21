from sqlalchemy import Column, Integer, String, Float
from database import Base

class LoanApplication(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String)
    income = Column(Float)
    loan_amount = Column(Float)
    risk_score = Column(Integer)
    status = Column(String)