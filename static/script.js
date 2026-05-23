const pinInput = document.getElementById("pin");

const mensajeDiv = document.querySelector(".mensaje");

const botones = document.querySelectorAll(".teclado button");


function agregar(numero){

    if(pinInput.disabled) return;

    pinInput.value += numero;
}


function limpiar(){

    if(pinInput.disabled) return;

    pinInput.value = "";
}


async function enviarPin(){

    if(pinInput.disabled) return;

    const formData = new FormData();

    formData.append("pin", pinInput.value);

    const response = await fetch("/validar", {

        method: "POST",
        body: formData

    });

    const data = await response.json();

    mensajeDiv.innerText = data.mensaje;

    // Bloquear teclado
    bloquearTeclado(data.ocupado);

    // Limpiar input
    pinInput.value = "";
}


function bloquearTeclado(bloquear){

    pinInput.disabled = bloquear;

    botones.forEach(boton => {

        boton.disabled = bloquear;

    });
}


async function actualizarEstado(){

    const response = await fetch("/estado");

    const data = await response.json();

    mensajeDiv.innerText = data.mensaje;

    bloquearTeclado(data.ocupado);
}


// Consultar estado cada segundo
setInterval(actualizarEstado, 3000);