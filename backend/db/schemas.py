from typing import Optional
from pydantic import BaseModel, ConfigDict

class PlayerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    JP_name: str
    position: str
    back_number: str
    team: str
    EN_name: Optional[str] = None 
    transfermarkt_URL: Optional[str] = None 

class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    task_type: str
    player_id: int
