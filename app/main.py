from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import engine
import time
from sqlalchemy.orm import Session

from .routers import post, user


# Telling passlib to use the bcrypt algorithm to encrypt passwords
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True: 
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', 
                            user='postgres', password='postgres',
                            row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error was:", error)
        time.sleep(2)
    
    
app.include_router(post.router)
app.include_router(user.router)    
# This is a path operation
# The / is just the root path operation
@app.get("/")
def main():
    return {"message": "Welcome to my "}




