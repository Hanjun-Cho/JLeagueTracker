from sqlalchemy.orm import Session
from db.models import Task

def get_task(db: Session, task_data: dict) -> Task | None:
    task = db.query(Task).filter(Task.name == task_data["name"]).first()
    return task

def get_all_tasks(db: Session) -> list:
    return db.query(Task).all()

def get_task_range(db: Session, offset: int, limit: int) -> list:
    return db.query(Task).offset(offset).limit(limit).all()

def get_task_count(db: Session) -> int:
    return db.query(Task).count()

def create_task(db: Session, task_data: dict) -> Task:
    if task := get_task(db, task_data):
        return task

    task = Task(
        name=task_data["name"],
        task_type=task_data["task_type"],
        player_id=task_data["player_id"]
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task
