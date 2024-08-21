from datetime import datetime
import math
from typing import Any, Dict
from uuid import UUID
from fastapi import Depends, APIRouter, Query
from starlette import status
from shared.type import PaginationResponse
from shared.exceptions import notfound_exception
from shared.database import get_db_context
from schemas.company import Company
from models.company import CompanyModel, CompanyViewModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/companies", tags=["Company"])


@router.get("/")
async def get_companies(
    db: Session = Depends(get_db_context),
    pageNumber: int = Query(1, description="Page number"),
    pageSize: int = Query(10, description="Number of companies to return per page"),
    status_code=status.HTTP_200_OK,
) -> PaginationResponse[CompanyViewModel]:
    total_companies = db.query(Company).count()

    totalPages = math.ceil(total_companies / pageSize)

    offset = (pageNumber - 1) * pageSize

    companies = db.query(Company).offset(offset).limit(pageSize).all()

    if not companies:
        raise notfound_exception("Company")

    company_view_models = [CompanyViewModel.from_orm(company) for company in companies]

    return {
        "pageNumber": pageNumber,
        "totalPages": totalPages,
        "pageSize": pageSize,
        "data": company_view_models,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_Company(
    request: CompanyModel, db: Session = Depends(get_db_context)
) -> None:
    company = Company(**request.dict())
    db.add(company)
    db.commit()


@router.put("/{company_id}", status_code=status.HTTP_200_OK)
async def update_Company(
    request: CompanyModel, company_id: UUID, db: Session = Depends(get_db_context)
) -> CompanyViewModel:
    company = db.query(Company).filter(Company.id == company_id).first()
    if Company is None:
        raise notfound_exception("Company")

    company.name = request.name
    company.description = request.description
    company.mode = request.mode
    company.rating = request.rating
    company.updated_at = datetime.utcnow()
    db.add(company)
    db.commit()
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID, db: Session = Depends(get_db_context)
) -> None:
    # Retrieve the company by its ID
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise notfound_exception("Company")

    # Delete the company
    db.delete(company)
    db.commit()
