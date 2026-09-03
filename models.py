from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Define a classe que se tornará a tabela 'tasks' no SQLite
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)