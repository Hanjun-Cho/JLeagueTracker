from sqlalchemy.orm import Session
from db.models import Player

def get_player(db: Session, id: int) -> Player | None:
    player = db.query(Player).filter(Player.id == id).first()
    return player

def create_player(db: Session, player_data: dict) -> Player:
    if player := get_player(db, player_data["id"]):
        return player

    player = Player(
        id=player_data["id"],
        JP_name=player_data["name"],
        position=player_data["position"],
        back_number=player_data["back_number"],
        team=player_data["team"],
        EN_name=None,
        transfermarkt_URL=None
    ) 

    db.add(player)
    db.commit()
    db.refresh(player)
    return player
