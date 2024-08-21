from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from shared.type import PaginationResponse
from schemas.user import User
from shared.exceptions import (
    badrequest_exception,
    forbidden_exception,
    notfound_exception,
)
from sqlalchemy.orm import Session
from shared.database import get_db_context
from schemas.task import Task
from models.task import TaskModel, TaskViewModel
from services import auth
import math

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskModel,
    current_user: User = Depends(auth.token_interceptor),
    db: Session = Depends(get_db_context),
) -> None:
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise forbidden_exception("User not found")

    new_task_data = request.dict()
    new_task_data["user_id"] = current_user.id

    new_task = Task(**new_task_data)

    db.add(new_task)
    db.commit()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_owner_task(
    db: Session = Depends(get_db_context),
    pageNumber: int = Query(1, description="Page number"),
    current_user: User = Depends(auth.token_interceptor),
    pageSize: int = Query(10, description="Number of tasks to return per page"),
    response_model=PaginationResponse[TaskViewModel],
) -> PaginationResponse[TaskViewModel]:
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    total_items = query.count()
    total_pages = math.ceil(total_items / pageSize)

    tasks = query.offset((pageNumber - 1) * pageSize).limit(pageSize).all()

    return {
        "pageNumber": pageNumber,
        "totalPages": total_pages,
        "pageSize": pageSize,
        "data": tasks,  # Convert tasks to TaskViewModel if needed
    }


# admin can get the list tasks of users (user email and id is in list tasks returned by admin)
@router.get("/get_user_tasks", status_code=status.HTTP_200_OK)
async def get_user_task(
    db: Session = Depends(get_db_context),
    pageNumber: int = Query(1, description="Page number"),
    current_user: User = Depends(auth.is_admin),
    pageSize: int = Query(10, description="Number of tasks to return per page"),
    response_model=PaginationResponse[Any],
) -> PaginationResponse[Any]:

    query = db.query(Task).join(User).filter(Task.owner_id == User.id)

    total_items = query.count()
    total_pages = math.ceil(total_items / pageSize)

    tasks = query.offset((pageNumber - 1) * pageSize).limit(pageSize).all()

    return {
        "pageNumber": pageNumber,
        "totalPages": total_pages,
        "pageSize": pageSize,
        "data": tasks,  # Convert tasks to TaskViewModel if needed
    }


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_information(
    task_id: UUID,
    request: TaskModel,
    db: Session = Depends(get_db_context),
    current_user: User = Depends(auth.token_interceptor),
) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise notfound_exception("Task")

    # Ensure the user can update this task (optional)
    if task.owner_id != current_user.id and not current_user.is_admin:
        raise forbidden_exception("You do not have permission to update this task")

    # Update the task fields
    for key, value in request.dict().items():
        setattr(task, key, value)

    db.commit()


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_information(
    task_id: UUID,
    db: Session = Depends(get_db_context),
    current_user: User = Depends(auth.token_interceptor),
) -> TaskViewModel:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise notfound_exception("Task")

    # Ensure the user can view this task (optional)
    if task.owner_id != current_user.id and not current_user.is_admin:
        raise forbidden_exception("You do not have permission to view this task")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db_context),
    current_user: User = Depends(auth.token_interceptor),
) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise notfound_exception("Task")

    if task.owner_id != current_user.id and not current_user.is_admin:
        raise forbidden_exception("You do not have permission to delete this task")

    db.delete(task)
    db.commit()
