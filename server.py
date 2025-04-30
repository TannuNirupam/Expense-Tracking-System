from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
from datetime import date
from typing import List
import db_helper  # this should have your database functions like insert, fetch, delete

app = FastAPI()

# -------------------------------
# Models
# -------------------------------

class Expense(BaseModel):
   
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

# -------------------------------
# Endpoints
# -------------------------------


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    """
    Get all expenses for a specific date.
    """
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=404, detail="Expenses not found")
  

@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    """
    Replace all expenses for a specific date.
    """
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(
                expense_date,
                expense.amount,
                expense.category,
                expense.notes
            )
        return {"message": "Expenses updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    """
    Get total and category breakdown of expenses between two dates.
    """
    summary_data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    
    if summary_data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

    total_amount = sum(row["total"] for row in summary_data)
    breakdown = {}

    for row in summary_data:
        percentage = (row["total"] / total_amount) * 100 if total_amount else 0
        breakdown[row["category"]] = {
            "total": row["total"],
            "percentage": percentage
        }

    return {
        "total": total_amount,
        "breakdown": breakdown
    }
