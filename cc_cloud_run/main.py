from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")

@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

  # get all votes from firestore collection
    votes = votes_collection.stream()
    vote_data = []
    tabs_count = 0
    spaces_count = 0
    
    # process the votes to count tabs/spaces and collect vote data
    for v in votes:
        vote_dict = v.to_dict()
        vote_data.append(vote_dict)
        
        # Count votes for tabs and spaces
        if vote_dict["team"] == "TABS":
            tabs_count += 1
        elif vote_dict["team"] == "SPACES":
            spaces_count += 1
    
    # sort recent votes by newest first
    vote_data.sort(key=lambda x: x["time_cast"], reverse=True)

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": spaces_count,
        "recent_votes": vote_data
    })

# Im trying to make a vote right now and Im getting an error. Im going to assume that its
# because i havent done the firestore stuff yet
@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================

    # create a new vote document in firestore
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")
    
    #create a new vote
    votes_collection.add(
        {
            "team":team,
            "time_cast": datetime.datetime.utcnow().isoformat()
        }
    )
    return {"success": True, "team": team}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
