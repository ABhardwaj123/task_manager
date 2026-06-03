function showTab(action) {
    //block makes thing visible
    //none hides it 
    if (action == 'login') {
        document.getElementById('login-form').style.display = 'block'
        document.getElementById('register-form').style.display = 'none'
    } else {
        document.getElementById('register-form').style.display = 'block'
        document.getElementById('login-form').style.display = 'none'
    }
}

//async is used to tell that function will do things that takes time
//if a function uses await -> must be async
async function login() {
    const email = document.getElementById('login-email').value
    const pass = document.getElementById('login-password').value

    //fetch sends HTTP request to our fastApi server
    //await means to wait until a response is generated
    const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
            //tells fastApi that we are sending data in json form
            'Content-Type': 'application/json'
        },
        //converts js object into json string
        body: JSON.stringify({ email, password: pass })
    })

    //converts the reponse to js object for accessing fields
    const data = await response.json()

    //localStorage is small storage in browser
    //setItem saves a key value pair
    //saving JWT token under the key "token"
    if (response.ok) {
        localStorage.setItem("token", data.access_token)

        //window is browser tab
        //redirecting the user
        window.location.href = "dashboard.html"
    } else {
        //grabs the div from our html (in html it is invisible)
        const msg = document.getElementById("message")
        //data.detail is the error message
        msg.innerText = data.detail
        //telling my css that error message has classname has "error"
        msg.className = "error"
    }
}

async function register() {

    const username = document.getElementById('register-username').value
    const email = document.getElementById('register-email').value
    const password = document.getElementById('register-password').value

    const response = await fetch('http://127.0.0.1:8000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })

    const data = await response.json()


    if (response.ok) {
        localStorage.setItem("token", data.access_token)
        window.location.href = "dashboard.html"
    } else {
        const msg = document.getElementById("message")
        msg.innerText = data.detail
        msg.className = "error"
    }
}

//functions for dashboard.html
function checkAuth() {
    const token = localStorage.getItem("token")

    if (!token) {
        window.location.href = "index.html"
    }
}

function logOut() {
    localStorage.removeItem("token")
    window.location.href = "index.html"
}

async function getTasks() {
    const token = localStorage.getItem("token")

    const response = await fetch("http://127.0.0.1:8000/tasks", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })

    const data = await response.json()
    renderTasks(data)
}


function renderTasks(data) {
    const container = document.getElementById("tasks-list");

    container.innerHTML = "";

    for (const task of data) {
        container.innerHTML += `
            <div class="task">
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <p>${task.is_done ? "Done" : "Pending"}</p>
                <button onclick="toggleTask(${task.id}, ${task.is_done})">
                    ${task.is_done ? "Undo" : "Complete"}
                </button>
                <button onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `
    }
}

async function toggleTask(id , status) {
    
    const token = localStorage.getItem("token")

    const response = await fetch(`http://127.0.0.1:8000/tasks/${id}` , {
        method: "PUT",
        headers: {
            "Content-Type": "application/json" ,
            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({is_done: !status})
    })

    if (response.ok) {
        getTasks()
    } else {
        const data = await response.json()
        const msg = document.getElementById("message")
        msg.innerText = data.detail
        msg.className = "error"
    }
}


async function deleteTask(id){

    const token = localStorage.getItem("token")

    const response = await fetch(`http://127.0.0.1:8000/tasks/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })

    if (response.ok) {
        getTasks()
    } else {
        const data = await response.json()
        const msg = document.getElementById("message")
        msg.innerText = data.detail
        msg.className = "error"
    }
}




async function addTask() {

    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    const token = localStorage.getItem("token")

    const response = await fetch("http://127.0.0.1:8000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, description })
    })

    const data = await response.json()

    if (response.ok) {
        //clear the inputs after adding
        document.getElementById('title').value = ""
        document.getElementById('description').value = ""
        // refresh the list
        getTasks()

    } else {
        const msg = document.getElementById("message")
        msg.innerText = data.detail
        msg.className = "error"
    }
}


if (document.getElementById('login-btn')) {
    document.getElementById('login-btn').addEventListener('click', login)
    document.getElementById('register-btn').addEventListener('click', register)
}

if (document.getElementById('logout-btn')) {
    checkAuth()
    document.getElementById('logout-btn').addEventListener('click', logOut)
    document.getElementById('addtask-btn').addEventListener('click', addTask)  
    getTasks()
}