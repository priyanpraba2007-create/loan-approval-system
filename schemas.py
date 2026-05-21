from pydantic import BaseModel, Field

class LoanCreate(BaseModel):
    # Field(...) ensures the number is greater than zero
    applicant_name: str
    income: float = Field(gt=0, description="Income must be greater than 0")
    loan_amount: float = Field(gt=0, description="Loan amount must be greater than 0")