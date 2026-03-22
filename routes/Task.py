from fastapi import APIRouter, HTTPException, Depends
from models.Task import Task as TaskModel, TaskUpdate
from config.db import db
from bson import ObjectId
from bson.errors import InvalidId
from utils.dependencies import get_current_user

route = APIRouter(prefix="/api/v1", tags=["Task"])

taskCollection = db["task"]


# ---------------- TRANSFORM ----------------
def transformTask(task) -> dict:
    return {
        "id": str(task.get("_id")),
        "title": task.get("title", ""),
        "desc": task.get("desc", ""),
        "is_complete": task.get("is_complete", False),
        "created_at": task.get("created_at")
    }


# ---------------- CREATE ----------------
@route.post("/create")
async def addTask(
    data: TaskModel,
    current_user: dict = Depends(get_current_user)
):
    task_dict = data.dict()

    # attach logged-in user
    task_dict["user_id"] = str(current_user["_id"])

    result = await taskCollection.insert_one(task_dict)

    task_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Task created successfully",
        "data": task_dict
    }


# ---------------- READ ----------------
@route.get("/get")
async def getAllTask(current_user: dict = Depends(get_current_user)):

    docs = taskCollection.find({
        "user_id": str(current_user["_id"])
    })

    tasks = []

    async for task in docs:
        tasks.append(transformTask(task))

    return tasks


# ---------------- UPDATE ----------------
@route.put("/update/{id}")
async def updateTask(
    id: str,
    data: TaskModel,
    current_user: dict = Depends(get_current_user)
):

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await taskCollection.update_one(
        {
            "_id": object_id,
            "user_id": str(current_user["_id"])
        },
        {"$set": data.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


# ---------------- PATCH ----------------
@route.patch("/patch/{id}")
async def patchTask(
    id: str,
    data: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    result = await taskCollection.update_one(
        {
            "_id": object_id,
            "user_id": str(current_user["_id"])
        },
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


# ---------------- DELETE ----------------
@route.delete("/delete/{id}")
async def deleteTask(
    id: str,
    current_user: dict = Depends(get_current_user)
):

    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await taskCollection.delete_one(
        {
            "_id": object_id,
            "user_id": str(current_user["_id"])
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}