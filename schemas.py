from pydantic import BaseModel
from typing import Optional

# Base comum para criação e leitura de tarefas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Dados esperados ao criar uma nova tarefa
class TaskCreate(TaskBase):
    pass

# Dados retornados pela API (inclui o ID e permite ler objetos do SQLAlchemy)
class TaskResponse(TaskBase):
    id: int
    class Config:
        from_attributes = True