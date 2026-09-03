// URL base da nossa API FastAPI
const API_URL = "http://127.0.0.1:8000/tasks";

// Elementos da interface (DOM)
const taskForm = document.getElementById("task-form");
const taskTitleInput = document.getElementById("task-title");
const taskDescInput = document.getElementById("task-desc");
const taskList = document.getElementById("task-list");
const taskCounter = document.getElementById("task-counter");
const filterButtons= document.querySelectorAll(".filter-btn");

// -------------------------------------------------------------
// Funções de Comunicação com a API (Fetch)
// -------------------------------------------------------------

// Variáveis de Estado (Memória da tela)
let allTasks = [];            
let currentFilter = "all";   
// Busca todas as tarefas da API e renderiza na tela

async function fetchTasks() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Erro ao buscar tarefas da API.");
        
        allTasks = await response.json();

        applyFilterAndRender();
    } catch (error) {
        console.error(error);
        taskList.innerHTML = `<li class="empty-state">Erro ao conectar com a API. Verifique se o servidor está rodando.</li>`;
    }
}


// Cria uma nova tarefa na API
async function createTask(title, description) {
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: description || null,
                completed: false
            })
        });

        if (!response.ok) throw new Error("Erro ao criar a tarefa.");
        
        // Recarrega a lista com os dados atualizados
        await fetchTasks();
    } catch (error) {
        console.error(error);
        alert("Não foi possível criar a tarefa.");
    }
}


// Atualiza o status de conclusão de uma tarefa existente
async function toggleTaskStatus(id, currentTitle, currentDesc, isCompleted) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: currentTitle,
                description: currentDesc,
                completed: isCompleted
            })
        });

        if (!response.ok) throw new Error("Erro ao atualizar o status da tarefa.");
        
        await fetchTasks();
    } catch (error) {
        console.error(error);
        alert("Não foi possível atualizar a tarefa.");
    }
}


//Remove uma tarefa pelo ID
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error("Erro ao excluir a tarefa.");
        
        await fetchTasks();
    } catch (error) {
        console.error(error);
        alert("Não foi possível deletar a tarefa.");
    }
}

// -------------------------------------------------------------
// Manipulação do DOM e Renderização
// -------------------------------------------------------------

// Filtra o array allTasks de acordo com o currentFilter e chama o renderTasks
function applyFilterAndRender() {
    let filteredTasks = allTasks;

    if (currentFilter === "pending") {

        filteredTasks = allTasks.filter(task => task.completed === false);
    } else if  (currentFilter === "completed") {
        
        filteredTasks = allTasks.filter(task => task.completed === true);
    }

    // Envia apenas a lista resultante para ser desenhada
    renderTasks(filteredTasks);
}

// Desenha os elementos na tela com base na lista de tarefas
function renderTasks(tasks) {
    taskList.innerHTML = "";
    taskCounter.textContent = `${tasks.length} ${tasks.length === 1 ? 'tarefa' : 'tarefas'}`;

    if (tasks.length === 0) {
        taskList.innerHTML = `<li class="empty-state">Nenhuma tarefa cadastrada. Comece adicionando uma acima! ✨</li>`;
        return;
    }

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = `task-item ${task.completed ? 'completed' : ''}`;

        li.innerHTML = `
            <div class="task-content">
                <input 
                    type="checkbox" 
                    ${task.completed ? 'checked' : ''} 
                    onchange="toggleTaskStatus(${task.id}, '${task.title}', '${task.description || ''}', this.checked)"
                >
                <div class="task-text">
                    <h3>${task.title}</h3>
                    ${task.description ? `<p>${task.description}</p>` : ''}
                </div>
            </div>
            <button class="btn-delete" title="Excluir tarefa" onclick="deleteTask(${task.id})">
                🗑️
            </button>
        `;

        taskList.appendChild(li);
    });
}

// -------------------------------------------------------------
// Eventos
// -------------------------------------------------------------

// Intercepta o envio do formulário
taskForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Impede o recarregamento padrão da página

    const title = taskTitleInput.value.trim();
    const description = taskDescInput.value.trim();

    if (title) {
        await createTask(title, description);
        taskForm.reset(); // Limpa os campos do formulário
        taskTitleInput.focus();
    }
});

// Carrega as tarefas assim que a página é aberta
document.addEventListener("DOMContentLoaded", fetchTasks);

