from sqlalchemy.orm import Session
from db.models import Player, Task

def remove_task(db: Session, id: int) -> Task | None:
    task = db.query(Task).filter(Task.id == id).first()

    if task is None:
        return None 

    db.delete(task)
    db.commit()
    return task

def get_task(db: Session, task_data: dict) -> Task | None:
    task = db.query(Task).filter(Task.name == task_data["name"]).first()
    return task

def get_all_tasks(db: Session) -> list:
    return db.query(Task).all()

def get_task_range(db: Session, offset: int, limit: int) -> list:
    return db.query(Task).offset(offset).limit(limit).all()

def get_task_count(db: Session) -> int:
    return db.query(Task).count()

def create_task(db: Session, name: str, task_type: str, player_id: int) -> Task:
    return create_task_dict(db, { "name": name, "task_type": task_type, "player_id": player_id })

def create_task_dict(db: Session, task_data: dict) -> Task:
    if task := get_task(db, task_data):
        return task

    task = Task(
        name=task_data["name"],
        task_type=task_data["task_type"],
        player_id=task_data["player_id"]
    )

    db.add(task)
    return task

# ------ helpers ------
def create_missing_EN_name_task(db: Session, player: Player) -> Task:
    return create_task(db, 
        f"{player.get_name()} is missing ENGLISH NAME",
        "MISSING EN_NAME",
        player.id
    )

def create_missing_transfermarkt_URL_task(db: Session, player: Player) -> Task:
    return create_task(db,
        f"{player.get_name()} is missing TRANSFERMARKT URL",
        "MISSING TRANSFERMARKT_URL",
        player.id
    )

def create_missing_dob_task(db: Session, player: Player) -> Task:
    return create_task(db,
        f"{player.get_name()} is missing DATE OF BIRTH",
        "MISSING DOB",
        player.id
    )

def create_missing_ordb_id_task(db: Session, player: Player) -> Task:
    return create_task(db,
        f"{player.get_name()} is missing ORDB ID",
        "MISSING ORDB_ID",
        player.id
    )

def create_missing_wyscout_id_task(db: Session, player: Player) -> Task:
    return create_task(db,
        f"{player.get_name()} is missing WYSCOUT ID",
        "MISSING WYSCOUT_ID",
        player.id
    )
