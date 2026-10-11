from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.users.models import UserModel


def create_task(body: TaskSchema,db: Session, user: UserModel):
    data = body.model_dump()
    task = TaskModel(title=data["title"], description=data["description"], is_completed=data["is_completed"], user_id = user.id)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def list_tasks(db: Session, user: UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks

def list_tasks_by_id(task_id: int, db: Session,user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorised ")
    return task

def update_task(task_id: int, body: TaskSchema, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorised")
    
    data = body.model_dump()
    for key,value in data.items():
        setattr(task, key, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


def delete_task(task_id: int, db: Session, user: UserModel):
    task = db.query(TaskModel).filter(TaskModel.user_id == user.id, TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorised")
    
    db.delete(task)
    db.commit()
    # db.refresh(task)
    
    return None