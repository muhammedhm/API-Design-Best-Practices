from fastapi import FastAPI
from src.utils.db import Base, engine
# from src.tasks.models import TaskModel
from src.tasks.router import tasks_router
from src.users.router import user_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", description="A simple task management API")
app.include_router(tasks_router)
app.include_router(user_router)