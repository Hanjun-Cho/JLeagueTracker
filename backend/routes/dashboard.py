from typing import List
import math
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.task_service import get_task_range, get_task_count
from db.schemas import TaskSchema
from db.db import get_session
dashboard_router = APIRouter()

PAGE_LIMIT = 30

@dashboard_router.get("/tasks", response_model=List[TaskSchema])
def get_tasks(page: int = 1, db: Session = Depends(get_session)) -> list:
    offset = PAGE_LIMIT * (page-1)
    tasks = get_task_range(db, offset, PAGE_LIMIT)
    return tasks

@dashboard_router.get("/tasks/max_page_count")
def get_task_max_page_count(db: Session = Depends(get_session)) -> int:
    count = get_task_count(db)
    return math.ceil(count / PAGE_LIMIT)
