# git_push.py

import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PushRequest(BaseModel):
    remote: str
    branch: str

@app.post("/push")
def push_changes(req: PushRequest):
    try:
        subprocess.run(["git", "push", req.remote, req.branch], check=True)
        return {"message": "Push successful"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class CommitRequest(BaseModel):
    message: str

@app.post("/commit")
def commit_changes(req: CommitRequest):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", req.message], check=True)
        return {"message": "Commit successful"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))    