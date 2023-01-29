// me ubido con el id del form
const taskForm = document.querySelector('#taskForm')


let tasks = []
editing = false
let taskId = null
// DOMContentLoaded es lo primero que se ejecuta cuando carga la pag
window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/tasks')
    const data = await response.json()
    tasks = data
    renderTask(tasks)
})


// escucho si sucede algun evento o click
taskForm.addEventListener('submit', async e => {
    e.preventDefault()

    // console.log(e) //veo el evento

    // obtengo el valor
    const title = taskForm["title"].value
    const task = taskForm["task"].value
    // const password = taskForm["password"].value

    console.log(title, task);

    if (!editing) {
      // funcion que envia al back-end
      const response = await fetch("/api/tasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title,
          task: task,
        }),
      });

      const data = await response.json(); // guardo la respuesta del POST y la muestro por consola
      // console.log(data)

      tasks.unshift(data); // añado al principio de la lista
    }else{
        const response = await fetch(`/api/tasks/${taskId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: title,
            task: task,
          }),
        });
        const updateTask = await response.json();
        console.log("update Task")
        console.log(updateTask)

        tasks = tasks.map(task => task.id === updateTask.id ? updateTask : task)

        editing = false
        taskId = null
    }
    
    // load tasks
    renderTask(tasks)

    // reseteo el formulario
    taskForm.reset()
})

function renderTask(){
    const taskList = document.querySelector('#taskList')
    taskList.innerHTML = ''

    tasks.forEach(task => {
      const taskItem = document.createElement("li");
      taskItem.classList = "list-group-item list-group-item-primary my-2"; //estilos del card
      // agrego con un for en el html
      taskItem.innerHTML = `
        <header class="d-flex justify-content-between align">
            <h3>${task.title}</h3>
            <div>
                <button class="btn-edit btn btn-primary btn-sm">Edit</button>
                <button class="btn-delete btn btn-danger btn-sm">Delete</button>
            </div>
        </header>
            <p>${task.task}</p>
        `;

      // Encuentro el id para eliminar
      const btnDelete = taskItem.querySelector(".btn-delete");

      btnDelete.addEventListener("click", async () => {
        const response = await fetch(`/api/tasks/${task.id}`, {
          method: "DELETE",
        });

        // convierto la respuesta y veo en consola
        const data = await response.json();
        
        // filtro la nueva list
        tasks = tasks.filter(task => task.id !== data.id)
        renderTask(tasks)
        });
        taskList.append(taskItem);

        
        // Editar
      const btnEdit = taskItem.querySelector(".btn-edit")

      btnEdit.addEventListener("click", async (e) => {
          const response = await fetch(`/api/tasks/${task.id}`)
          const data = await response.json()

          console.log(data)
        
          taskForm["title"].value = data[1];
          taskForm["task"].value = data[2];

          editing = true
          taskId = data[0]
          console.log(taskId)

      })
    })
}
