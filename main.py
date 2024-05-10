from fastapi import FastAPI
from tracker import main


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tracker")
async def tracker(name: str):
    print(name)
    return  main(name)


