from typing import List

from fastapi import APIRouter,Depends,status
from src.tasks import controller
from src.tasks.dtos import TaskResponseSchema, TaskSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.users.models import UserModel

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@tasks_router.post("/create",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED,summary="Create a new task", description="Create a new task with the provided title and description.")
def create_task(body: TaskSchema, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.create_task(body,db,user)


@tasks_router.get("/list",response_model=List[TaskResponseSchema] ,status_code=status.HTTP_200_OK,summary="List all tasks", description="Retrieve a list of all tasks.")
def list_tasks(db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.list_tasks(db,user)

@tasks_router.get("/listbyID/{task_id}",response_model=TaskResponseSchema ,status_code=status.HTTP_200_OK, summary="List all tasks by ID", description="Retrieve a list of all tasks by ID.")
def list_tasks_by_id(task_id: int, db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.list_tasks_by_id(task_id, db,user)

@tasks_router.get("/listbyID", response_model=TaskResponseSchema ,status_code=status.HTTP_200_OK, summary="List all tasks by ID", description="Retrieve a list of all tasks by ID.")
def list_tasks_by_id_query(task_id: int, db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.list_tasks_by_id(task_id, db,user)

@tasks_router.put("/update/{task_id}", status_code=status.HTTP_201_CREATED, summary="Update a task", description="Update an existing task with the provided title and description.")
def update_task(task_id: int, body: TaskSchema, db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.update_task(task_id, body, db, user)

@tasks_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task", description="Delete an existing task by its ID.")
def delete_task(task_id: int, db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.delete_task(task_id, db, user)