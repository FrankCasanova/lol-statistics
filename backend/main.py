from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .tracker import main


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/playerprofile-data{name}")
async def tracker(name: str):
    print(name)
    return await main(name)


