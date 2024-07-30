# sonar_integration.py

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

SONARQUBE_API_URL = "your_sonarqube_api_url"
SONARQUBE_API_TOKEN = "your_sonarqube_api_token"

AI_CODE_REVIEW_API_URL = "your_ai_code_review_api_url"
AI_CODE_REVIEW_API_KEY = "your_ai_code_review_api_key"

@app.post("/sonar-review")
async def sonar_review():
    headers = {
        "Authorization": f"Bearer {SONARQUBE_API_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SONARQUBE_API_URL}/api/qualitygates/project_status?projectKey=your_project_key", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching SonarQube data")


@app.post("/ai-code-review")
async def ai_code_review(code: str):
    headers = {
        "Authorization": f"Bearer {AI_CODE_REVIEW_API_KEY}"
    }
    json_payload = {"code": code}
    async with httpx.AsyncClient() as client:
        response = await client.post(AI_CODE_REVIEW_API_URL, json=json_payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching AI code review")