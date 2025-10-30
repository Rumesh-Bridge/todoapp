from fastapi import FastAPI

#Create an instance of the FastAPI class
app = FastAPI()

@app.get("/")
def read_root():
    return {'message':"Hello, FastAPI!"}

