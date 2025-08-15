from fastapi import FastAPI


app =  FastAPI()


@app.get("/")
def read_root():
    return {"method": "GET", "message": "Hello from GET!"}

@app.post("/")
def create_root():
    return {"method": "POST", "message": "Hello from POST!"}
