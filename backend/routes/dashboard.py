from typing import List
import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas import PlayerSchema
from service.player_service import get_player, update_EN_Name
from service.task_service import get_task_range, get_task_count, remove_task
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

@dashboard_router.get("/players", response_model=PlayerSchema)
def get_player_by_id(id: int, db: Session = Depends(get_session)) -> PlayerSchema:
    player = get_player(db, id)

    if player is None:
        raise HTTPException(status_code=404, detail=f"Player with ID {id} not found")
    else:
        return player

@dashboard_router.put("/players/update_EN_name", response_model=PlayerSchema)
def update_player_EN_Name(id: int, EN_name: str, db: Session = Depends(get_session)) -> PlayerSchema:
    player = update_EN_Name(db, id, EN_name)

    if player is None:
        raise HTTPException(status_code=404, detail=f"Player with ID {id} not found")
    else:
        return player

@dashboard_router.delete("/tasks/delete", response_model=TaskSchema)
def delete_task(id: int, db: Session = Depends(get_session)) -> TaskSchema:
    task = remove_task(db, id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
    else:
        return task
