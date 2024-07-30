# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github_auth import get_repositories
from git_push_commit import CommitRequest, push_changes,commit_changes
from sonar_integration import sonar_review,ai_code_review

app = FastAPI()

class PushRequest(BaseModel):
    message: str
    remote: str
    branch: str
    code: str

@app.get("/github/repositories")
async def fetch_repositories(code: str):
    return await get_repositories(code=code)

@app.post("/commit")
def commit_changes_endpoint(req: CommitRequest):
    return commit_changes(req)

@app.post("/push")
def push_changes_endpoint(req: PushRequest):
    return push_changes(req)

@app.post("/sonar-review")
async def sonar_review_endpoint():
    return await sonar_review()

@app.post("/ai-code-review")
async def ai_code_review_endpoint(code: str):
    return await ai_code_review(code)

@app.post("/process-and-push")
async def process_and_push(req: PushRequest):
    # Commit changes
    commit_response = commit_changes(req.message)
    
    # Perform SonarQube review
    sonar_response = await sonar_review()
    
    if sonar_response.get("status") == "failed":
        raise HTTPException(status_code=400, detail="SonarQube review failed")
    
    # Perform AI-based code review
    ai_review_response = await ai_code_review(req.code)
    
    # Print or log AI review response
    print(ai_review_response)

    # Push changes
    push_response = push_changes(req)
    
    return {"message": "Process completed successfully", "commit": commit_response, "push": push_response}
