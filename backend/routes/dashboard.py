from typing import List, Optional
import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas import PlayerSchema
from service.player_service import get_player, update_EN_Name, update_dob, update_ordb_id, update_transfermarkt_URL, update_wyscout_id
from service.task_service import get_task_range, get_task_count, remove_task
from db.schemas import TaskSchema
from db.db import get_session
from pydantic import BaseModel
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

@dashboard_router.delete("/tasks/delete", response_model=TaskSchema)
def delete_task(id: int, db: Session = Depends(get_session)) -> TaskSchema:
    task = remove_task(db, id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
    else:
        return task

@dashboard_router.get("/players", response_model=PlayerSchema)
def get_player_by_id(id: int, db: Session = Depends(get_session)) -> PlayerSchema:
    player = get_player(db, id)

    if player is None:
        raise HTTPException(status_code=404, detail=f"Player with ID {id} not found")
    else:
        return player

class PlayerPatch(BaseModel):
    EN_name: Optional[str] = None
    transfermarkt_URL: Optional[str] = None
    date_of_birth: Optional[str] = None
    ordb_id: Optional[str] = None
    wyscout_id: Optional[str] = None

@dashboard_router.patch("/players/update_player", response_model=PlayerSchema)
def update_player(id: int, data: PlayerPatch, db: Session = Depends(get_session)):
    if data.EN_name is not None:
        update_EN_Name(db, id, data.EN_name) 

    if data.transfermarkt_URL is not None:
        update_transfermarkt_URL(db, id, data.transfermarkt_URL)

    if data.date_of_birth is not None:
        update_dob(db, id, data.date_of_birth, format="%Y-%m-%d")

    if data.ordb_id is not None:
        update_ordb_id(db, id, data.ordb_id)

    if data.wyscout_id is not None:
        update_wyscout_id(db, id, data.wyscout_id)

    if player := get_player(db, id):
        db.commit()
        return player

    raise HTTPException(status_code=404, detail=f"Player with ID {id} not found")
