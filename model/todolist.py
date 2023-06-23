# 导入需要的模块
import enum  # 枚举模块
from typing import Optional  # 类型提示模块

# 导入SQLModel类和Field类
from sqlmodel import Field, SQLModel


# 创建枚举类States
class States(enum.Enum):
    normal = 1  # 状态1
    success = 2  # 状态2
    delete = 3  # 状态3


# 创建ToDoBase类，并继承SQLModel类
class ToDoBase(SQLModel):
    title: str  # 标题
    description: str  # 描述
    completed: bool  # 是否完成


# 创建ToDo类，并继承ToDoBase和SQLModel类，并将其设为表
class ToDo(ToDoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # id字段为可选的整数类型，如果为None，则使用默认主键


# 创建ToDoRead类，继承ToDoBase类，加入含有id字段的属性
class ToDoRead(ToDoBase):
    id: int  # id


# 创建ToDoCreate类，继承ToDoBase类
class ToDoCreate(ToDoBase):
    pass


# 创建ToDoUpdate类，继承SQLModel类，包含标题、描述、完成状态三个属性
class ToDoUpdate(SQLModel):
    title: str  # 标题
    description: str  # 描述
    completed: bool  # 是否完成
