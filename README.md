# 📋 Task Manager - API & Web Interface (Full Stack)

Uma aplicação Full Stack completa para gerenciamento de tarefas cotidianas, construída com foco em arquitetura limpa, tipagem estática, persistência relacional e interface responsiva.

---

## Tecnologias Utilizadas

### Back-end

- **Python 3.10+**
- **FastAPI:** Framework web moderno de alto desempenho para construção de APIs RESTful.
- **SQLAlchemy:** ORM para abstração e comunicação com banco de dados relacional.
- **SQLite:** Banco de dados relacional em arquivo para persistência local.
- **Pydantic:** Validação rigorosa de esquemas de entrada e saída de dados.
- **Uvicorn:** Servidor ASGI para execução assíncrona da aplicação.
- **Pytest & HTTPX:** Bateria de testes automatizados para validação de endpoints.

### Front-end

- **HTML5:** Estrutura semântica e acessível.
- **CSS3:** Layout moderno, responsivo (Flexbox) e estilização de estados dinâmicos.
- **JavaScript (Vanilla / ES6+):** Manipulação assíncrona do DOM via `fetch API` com `async/await`.

---

## Funcionalidades

- [x] Listagem de todas as tarefas cadastradas.
- [x] Criação de novas tarefas com validação de campos obrigatórios.
- [x] Atualização de status de conclusão (concluído / pendente) com um clique.
- [x] Exclusão permanente de tarefas do banco de dados.
- [x] Filtragem dinâmica na interface (Todas, Pendentes, Concluídas) no lado do cliente.
- [x] Suporte a CORS configurado para integração cliente-servidor.
- [x] Suíte de testes automatizados cobrindo os fluxos principais da API.

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado na sua máquina.
- Git configurado.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/LuizLoss/task-manager-fullstack.git](https://github.com/LuizLoss/task-manager-fullstack.git)
cd task-manager-fullstack
```
