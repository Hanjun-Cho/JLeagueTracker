from datetime import datetime
from sqlalchemy.orm import Session
from db.models import Player

def update_EN_Name(db: Session, id: int, EN_name: str) -> Player | None:
    if player := get_player(db, id):
        player.EN_name = EN_name
        return player
    return None

def update_transfermarkt_URL(db: Session, id: int, transfermarkt_URL: str) -> Player | None:
    if player := get_player(db, id):
        player.transfermarkt_URL = transfermarkt_URL 
        return player
    return None

def update_dob(db: Session, id: int, dob: str, format: str = "%d/%m/%Y") -> Player | None:
    if player := get_player(db, id):
        date_obj = datetime.strptime(dob, format).date()
        player.date_of_birth = date_obj 
        return player
    return None

def update_ordb_id(db: Session, id: int, ordb_id: str) -> Player | None:
    if player := get_player(db, id):
        player.ordb_id = ordb_id 
        return player
    return None

def update_wyscout_id(db: Session, id: int, wyscout_id: str) -> Player | None:
    if player := get_player(db, id):
        player.wyscout_id = wyscout_id 
        return player
    return None

def get_player(db: Session, id: int) -> Player | None:
    player = db.query(Player).filter(Player.id == id).first()
    return player

def get_player_by_team_and_number(db: Session, team_id: str, back_number: str) -> Player | None:
    player = db.query(Player).filter(Player.team_id == team_id, Player.back_number == back_number).first();
    return player

def get_player_link(db: Session, name: str, dob: str, team_id: str) -> Player | None:
    date_obj = datetime.strptime(dob, "%m/%d/%Y").date()
    player = db.query(Player).filter(Player.EN_name == name, Player.date_of_birth == date_obj, Player.team_id == team_id).first()
    return player

def get_players_from_team(db: Session, team: str) -> list:
    return db.query(Player).filter(Player.team == team).all()

def create_player(db: Session, player_data: dict) -> Player:
    if player := get_player(db, player_data["id"]):
        return player

    player = Player(
        id=player_data["id"],
        JP_name=player_data["name"],
        position=player_data["position"],
        back_number=player_data["back_number"],
        team=player_data["team"],
        team_id=player_data["team_id"],
        EN_name=None,
        transfermarkt_URL=None
    ) 

    db.add(player)
    return player
