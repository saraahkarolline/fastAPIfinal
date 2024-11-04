from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from faker import Faker
from typing import List
from passlib.context import CryptContext
from fastapi.responses import HTMLResponse
import pandas as pd
from Levenshtein import distance

app = FastAPI()
fake = Faker()
security = HTTPBasic()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

hashed_password = pwd_context.hash("password1")

fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "Usuario Um",
        "email": "user1@example.com",
        "hashed_password": hashed_password, 
    }
}

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = fake_users_db.get(credentials.username)
    if user is None or not pwd_context.verify(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="senha ou login incorreto",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/fake-names", response_model=List[str])
def read_fake_names(username: str = Depends(get_current_username)):
    names = [fake.name() for _ in range(10)]
    return names

@app.get("/resultado", response_class=HTMLResponse)
def resultado(username: str = Depends(get_current_username)):
    names = [fake.name() for _ in range(10)]
    origem_nome = names[0]
    distances = [(name, distance(origem_nome, name)) for name in names[1:]]
    df = pd.DataFrame(distances, columns=["Nome", "Distância para origem"])
    df = df.sort_values(by="Distância para origem")

    html_content = df.to_html(index=False)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/tests")
def test():
    return {"message": "teste!"}
