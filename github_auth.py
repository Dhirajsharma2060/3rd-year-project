# github_auth.py

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request
import httpx

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token"
)

GITHUB_CLIENT_ID = "your_github_client_id"
GITHUB_CLIENT_SECRET = "your_github_client_secret"

async def get_github_access_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"}
        )
        response_data = response.json()
        return response_data.get("access_token")

@app.get("/github/repositories")
async def get_repositories(request: Request, code: str = Depends(oauth2_scheme)):
    token = await get_github_access_token(code)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {token}"}
        )
        return response.json()
