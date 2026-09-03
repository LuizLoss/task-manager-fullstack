from fastapi.testclient import TestClient
from main import app

# Inicializa o cliente de testes
client = TestClient(app)


def test_read_home():
    """Valida se a rota inicial responde com status 200 e a mensagem correta."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de Tarefas funcionando com sucesso!"}


def test_create_and_read_task():
    """Valida a criação e leitura individual de uma tarefa."""
    payload = {
        "title": "Estudar Testes com Pytest",
        "description": "Praticar escrita de testes automatizados",
        "completed": False
    }
    
    # 1. Cria a tarefa
    post_response = client.post("/tasks", json=payload)
    assert post_response.status_code == 201
    
    created_task = post_response.json()
    assert created_task["title"] == payload["title"]
    assert "id" in created_task
    
    task_id = created_task["id"]
    
    # 2. Busca a tarefa criada pelo ID
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id


def test_get_nonexistent_task():
    """Valida se uma tarefa inexistente retorna erro 404."""
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    # Valida que o detalhe do erro contém a mensagem padrão
    assert response.json()["detail"] == "Tarefa com ID 99999 não encontrada."


def test_delete_task():
    """Valida o fluxo de remoção de uma tarefa."""
    # Cria uma tarefa temporária
    temp_task = client.post("/tasks", json={
        "title": "Tarefa descartável",
        "description": "Criada apenas para teste de delete",
        "completed": False
    }).json()
    
    task_id = temp_task["id"]
    
    # Remove a tarefa criada
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # Confirma que ela não existe mais
    check_response = client.get(f"/tasks/{task_id}")
    assert check_response.status_code == 404