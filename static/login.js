
async function loginUser(){
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch('/token',{
        method: 'POST',
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${username}&password=${password}`
    });

    if (response.ok){
        const data= await response.json();
        if (data){
            window.location.href='/dashboard'
        } else {
            alert('Credenciales incorrectas')
        }
    }
}