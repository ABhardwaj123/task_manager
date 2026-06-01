function showTab(action){
    //block makes thing visible
    //none hides it 

    if(action == 'login'){
        document.getElementById('login-form').style.display = 'block'
        document.getElementById('register-form').style.display = 'none'
    }else{
        document.getElementById('register-form').style.display = 'block'
        document.getElementById('login-form').style.display = 'none'
    }
}

//async is used to tell that function will do things that takes time
//if a function uses await -> must be async
async function login(){
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
        body: JSON.stringify({email , password: pass})
    })

    //converts the reponse to js object for accessing fields
    const data = await response.json()

    //localStorage is small storage in browser
    //setItem saves a key value pair
    //saving JWT token under the key "token"
    if(response.ok){
        localStorage.setItem("token" , data.access_token)

        //window is browser tab
        //redirecting the user
        window.location.href = "dashboard.html"
    }else{
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

    const response = await fetch('http://127.0.0.1:8000/auth/register' , {
        method: 'POST' ,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username , email , password})
    })

    const data = await response.json()


    if(response.ok){
        localStorage.setItem("token" , data.access_token)
        window.location.href = "dashboard.html"
    }else{
        const msg = document.getElementById("message")
        msg.innerText = data.detail
        msg.className = "error"
    }
}

//when login button is clicked then run the login function
document.getElementById('login-btn').addEventListener('click', login)
document.getElementById('register-btn').addEventListener('click', register)