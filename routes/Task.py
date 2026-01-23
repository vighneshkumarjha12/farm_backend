from fastapi import APIRouter, HTTPException
from models.Task import Task as TaskModel
from config.db import db
from bson import ObjectId
from bson.errors import InvalidId
from models.Task import Task, TaskUpdate

route = APIRouter(prefix="/api/v1", tags=["Task"])

taskCollection = db["task"]

# ---------------- CREATE ----------------
@route.post("/create")
async def addTask(data: TaskModel):
    task_dict = data.dict()
    result = await taskCollection.insert_one(task_dict)

    task_dict["_id"] = str(result.inserted_id)

    return {
        "message": "Task created successfully",
        "data": task_dict
    }


# ---------------- TRANSFORM ----------------
def transformTask(task) -> dict:
    return {
        "id": str(task.get("_id")),
        "title": task.get("title", ""),
        "desc": task.get("desc", ""),
        "is_complete": task.get("is_complete", False),
        "created_at": task.get("created_at")
    }


# ---------------- READ ----------------
@route.get("/get")
async def getAllTask():
    docs = taskCollection.find({})
    tasks = []

    async for task in docs:
        tasks.append(transformTask(task))

    return tasks


# ---------------- UPDATE (PUT) ----------------
@route.put("/update/{id}")
async def updateTask(id: str, data: TaskModel):
    result = await taskCollection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}


# ---------------- PARTIAL UPDATE (PATCH) ----------------
@route.patch("/patch/{id}")
async def patchTask(id: str, data: TaskUpdate):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    result = await taskCollection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task updated successfully"}

# ---------------- DELETE ----------------
@route.delete("/delete/{id}")
async def deleteTask(id: str):
    result = await taskCollection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
