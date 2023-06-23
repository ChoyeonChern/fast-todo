from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from fastapi.middleware.cors import CORSMiddleware
from routers import todolist
from setting.database import engine
from model.todolist import ToDo


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问，可以根据需求更改为特定的域名列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    todos = [ToDo(title="吃饭", description="Description 吃饭", completed=False),
             ToDo(title="学习", description="Description 学习", completed=False),
             ToDo(title="运动", description="Description 运动", completed=True),
             ToDo(title="睡觉", description="Description 睡觉", completed=True)
             ]
    with Session(engine) as session:
        session.add_all(todos)
        session.commit()


app.include_router(todolist.router)
