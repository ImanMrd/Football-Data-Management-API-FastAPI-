## calling necessary libiraries to impelement the code


from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from auth import require_admin
from auth import router as auth_router
app = FastAPI()
app.include_router(auth_router)

# —————————————
# Database setup
# —————————————


## creating database and starting the engine to store the data

DATABASE_URL = "sqlite:///./football.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    init_db()

# —————————————
# Creating entities / defining each entity
# —————————————


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    foundation_year: int
    city: str


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_date: str 
    role_id: int = Field(foreign_key="playerrole.id")

class PlayerHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
    start_date: str        # when the player joined the team
    end_date: Optional[str] = None      # when they left (can be ongoing)

class PlayerRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "goalkeeper", "midfielder"


# —————————————
# TEAM Endpoints
# —————————————
@app.post("/teams/", dependencies=[Depends(require_admin)])  #create a team / only by admin
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team) # add to session
    session.commit()  # save into session
    session.refresh(team)  # uodate the session
    return team

@app.put("/teams/{team_id}", dependencies=[Depends(require_admin)]) # update a team / only by admin
def update_team(team_id: int, team: Team, session: Session = Depends(get_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")   # if the data is not in the database show the error (team not found)
    db_team.name = team.name
    db_team.foundation_year = team.foundation_year
    db_team.city = team.city
    session.add(db_team)  # add to session
    session.commit()  # save into session
    session.refresh(db_team)  # uodate the session
    return db_team

@app.delete("/teams/{team_id}", dependencies=[Depends(require_admin)])  # delete a team only by admin
def delete_team(team_id: int, session: Session = Depends(get_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(db_team)  #delete the session
    session.commit()  # uodate the session
    return {"ok": True}


# ------------------
# Player Endpoints
# ------------------

@app.post("/players/", dependencies=[Depends(require_admin)])  #create a player / only by admin
def create_player(player: Player, session: Session = Depends(get_session)):
    session.add(player) # add to session
    session.commit()
    session.refresh(player)
    return player

@app.put("/players/{player_id}", dependencies=[Depends(require_admin)])  #updating a player
def update_player(player_id: int, player: Player, session: Session = Depends(get_session)):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found") # if player is not in the database, show the error ( player not found)
    db_player.name = player.name
    db_player.birth_date = player.birth_date
    db_player.role_id = player.role_id
    session.commit()  # save into session
    return db_player

@app.delete("/players/{player_id}", dependencies=[Depends(require_admin)]) # delete a player by admin
def delete_player(player_id: int, session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    session.delete(player)
    session.commit()
    return {"ok": True}


# ------------------
# PlayerRole Endpoints
# ------------------

@app.post("/roles/", dependencies=[Depends(require_admin)]) #create a player role / only by admin
def create_role(role: PlayerRole, session: Session = Depends(get_session)):
    session.add(role) # add to session
    session.commit()  # save into session
    session.refresh(role) # uodate the session
    return role

@app.put("/roles/{role_id}", dependencies=[Depends(require_admin)]) # update a player role only by admin
def update_role(role_id: int, role: PlayerRole, session: Session = Depends(get_session)):
    db_role = session.get(PlayerRole, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.name = role.name
    session.commit() # save into session
    return db_role

@app.delete("/roles/{role_id}", dependencies=[Depends(require_admin)]) # delete player role only by admin
def delete_role(role_id: int, session: Session = Depends(get_session)):
    db_role = session.get(PlayerRole, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    session.delete(db_role) # delete the session   
    session.commit()  # save into session
    return {"ok": True}

@app.get("/roles/", response_model=List[PlayerRole])  # loading the data / reading data
def list_roles(session: Session = Depends(get_session)):
    return session.exec(select(PlayerRole)).all()

# ------------------
# Player History Endpoints
# ------------------

@app.post("/player-history/", dependencies=[Depends(require_admin)]) #create a player history / only by admin
def add_player_history(history: PlayerHistory, session: Session = Depends(get_session)):
    session.add(history)
    session.commit()
    session.refresh(history)
    return history

@app.get("/players/{player_id}/history", response_model=List[PlayerHistory])  # loading the data / reading data
def get_player_history(player_id: int, session: Session = Depends(get_session)):
    stmt = select(PlayerHistory).where(PlayerHistory.player_id == player_id)
    history = session.exec(stmt).all()
    return history