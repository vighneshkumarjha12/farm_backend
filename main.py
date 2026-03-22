from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers
from routes import auth
from routes.Task import route as TaskRoute

app = FastAPI(title="Task Manager")

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router)
app.include_router(TaskRoute)

# root route
@app.get("/")
def indexView():
    return {
        "msg": "Hi Task Manager API is running 🚀"
    }