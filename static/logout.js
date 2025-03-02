
async function logout(){
    const response =  await fetch('/logout',{
        method:'POST',
        credentials: 'include'
    })

    if (response.ok){
        window.location.href='/';
    } else {
        alert('Ha habido un error')
    }
    alert('Tu sesion ha expirado')
    window.location.href='/';
}