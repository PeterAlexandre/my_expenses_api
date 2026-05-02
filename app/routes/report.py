from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_session
from app.models.user import User
from app.schemas.report import MonthlyReport
from app.security import get_current_user
from app.services.report_service import get_monthly_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly", response_model=MonthlyReport)
def monthly(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    month: int = Query(default=None, ge=1, le=12),
    year: int = Query(default=None, ge=2000),
):
    today = date.today()
    return get_monthly_report(
        session,
        current_user,
        year=year or today.year,
        month=month or today.month,
    )
