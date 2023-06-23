from typing import List

from fastapi import Depends, APIRouter, HTTPException, Query
from sqlmodel import Session, select

from dependencies.dependencies import get_session
from model.todolist import ToDo, ToDoRead, ToDoUpdate, ToDoCreate

#  创建一个路由对象，指定前缀为  /api
router = APIRouter(prefix="/api")


#  创建读取todos数据的接口
@router.get("/todos/", response_model=List[ToDoRead])
def read_todos(
        *,
        session: Session = Depends(get_session),  # 依赖注入，获取数据库连接
        offset: int = 0,  # 分页查询参数：偏移量
        limit: int = Query(default=100, lte=100),  # 分页查询参数：每页数量，最大值为100
):
    #  从数据库中选择  todos  数据，并使用  offset  和  limit  来进行分页查询
    todos = session.exec(select(ToDo).offset(offset).limit(limit)).all()
    return todos


#  创建读取单个  todo  数据的接口
@router.get("/todo/{ToDo_id}", response_model=ToDoRead)
def read_todo(*, session: Session = Depends(get_session), ToDo_id: int):
    #  从数据库中获取指定  id  的  todo  数据
    todo = session.get(ToDoRead, ToDo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")  # 如果没有找到该数据，则返回  404  错误
    return todo


#  创建新增  todo  数据的接口
@router.post("/todo/", response_model=ToDoRead)
def creat_todo(*, session: Session = Depends(get_session), todo: ToDoCreate):
    #  将传入的  ToDoCreate  对象转换为  SQLModel  对象，并将其添加到数据库中
    db_todo = ToDo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)  # 刷新当前会话，使新数据生效
    return db_todo  # 返回新创建的数据


#  创建更新  todo  数据的接口
@router.patch("/todo/{ToDo_id}", response_model=ToDoUpdate)
def update_todo(
        *,
        session: Session = Depends(get_session),  # 依赖注入，获取数据库连接
        ToDo_id: int,  # 待更新数据的  id
        todo_update: ToDoUpdate,  # 更新后的数据
):
    db_todo = session.get(ToDo, ToDo_id)  # 获取待更新数据
    if not db_todo:
        raise HTTPException(status_code=404, detail="ToDo    not    found")
    todo_data = todo_update.dict(exclude_unset=True)  # 将传入数据转换为字典
    #  更新已有数据
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)  # 刷新当前会话，使更新数据生效
    return db_todo  # 返回更新后的数据


#  创建删除  todo  数据的接口
@router.delete("/todo/{ToDo_id}")
def delete_todo(*, session: Session = Depends(get_session), ToDo_id: int):
    #  获取待删除数据
    todo = session.get(ToDo, ToDo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo    not    found")
    session.delete(todo)  # 从数据库中删除数据
    session.commit()
    return {"ok": True}  # 返回操作成功的标志
