from db.models import Team
from sqlalchemy.orm import Session

def get_team(db: Session, id: int) -> Team | None:
    team = db.query(Team).filter(Team.id == id).first()
    return team

def create_team(db: Session, team_name: str, team_data: dict) -> Team:
    if team := get_team(db, team_data["id"]):
        return team

    team = Team(
        id=team_data["id"],
        JP_name=team_data["JP_name"],
        EN_name=team_name,
        injury_tracker_id=team_data["injury_tracker"],
        transfermarkt=team_data["transfermarkt"],
        wyscout_name=team_data["wyscout_name"],
        ordb_name=team_data["ordb_name"]
    )

    db.add(team)
    return team
