from typing import Union

from fastapi import FastAPI

from routes.Task import route as TaskRoute

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title= "Task Manager")

origins = [
    "*"
     
]
app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(TaskRoute)

@app.get("/")
def indexView():
    return{
        "mag"  : "hi vighnesh"
    }