from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# 1. Cria as tabelas no SQLite se não existirem
models.Base.metadata.create_all(bind=engine)

# 2. Inicialização da aplicação
app = FastAPI(
    title="Task Manager API com SQLite",
    description="API para gerenciar tarefas com persistência em SQLite",
    version="1.1.0"
)

# 3. Configuração do Middleware de CORS
# Permite que qualquer página web local faça requisições para a nossa API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Permite requisições de qualquer origem (ideal para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],            # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],            # Permite todos os cabeçalhos HTTP
)

# -------------------------------------------------------------
# Endpoints da API
# -------------------------------------------------------------

@app.get("/", tags=["Geral"])
def home():
    """Retorna mensagem de boas-vindas padronizada."""
    return {"message": "API de Tarefas funcionando com sucesso!"}


@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["Tarefas"])
def list_tasks(db: Session = Depends(get_db)):
    """Lista todas as tarefas cadastradas no banco."""
    return db.query(models.TaskModel).all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tarefas"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Busca uma tarefa específica pelo ID."""
    task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada."
        )
    return task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Cadastra uma nova tarefa no banco de dados."""
    db_task = models.TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tarefas"])
def update_task(task_id: int, task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Atualiza o título, descrição ou status de conclusão de uma tarefa."""
    db_task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada para atualização."
        )
    
    db_task.title = task_data.title
    db_task.description = task_data.description
    db_task.completed = task_data.completed

    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tarefas"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Remove permanentemente uma tarefa do banco."""
    db_task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada para exclusão."
        )
    
    db.delete(db_task)
    db.commit()
    return