function mostrarCargador() {
    Swal.fire({
        title: 'Cargando...',
        text: 'Por favor espere, estamos trabajando en ello... 😊',
        icon: 'info',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        willOpen: () => {
            Swal.showLoading();
        }
    });
}


function ocultarCargador() {
    Swal.close();
}

function alertaMensaje(tipo, mensaje) {
    Swal.fire({
        icon: tipo,
        title: 'Aviso',
        html: `<span class="fs-2">${mensaje}</span>`,
        confirmButtonText: "Aceptar",
        customClass: {
            confirmButton: 'btn btn-primary',
        },
        allowOutsideClick: false,
        allowEscapeKey: false
    });
}

const alertaRecarga = (tipo, mensaje) => {
    Swal.fire({
        icon: tipo,
        title: 'Aviso',
        html: `<span class="fw-bold fs-5">${mensaje}</span>`,
        showConfirmButton: true,
        confirmButtonText: 'Aceptar',
        customClass: {
            confirmButton: 'btn btn-primary',
        },
        allowOutsideClick: false,
        allowEscapeKey: false
    })
        .then(res => {
            if (res.isConfirmed) {
                location.reload();
            }
        });
}

const bloquearElemento = (elemento, duracion = 3000) => {
    if (!elemento) return;

    const objeto = document.querySelector(elemento);

    objeto.setAttribute('disabled', true);
    objeto.style.pointerEvents = 'none';
    objeto.style.opacity = '0.5';
    objeto.style.cursor = 'not-allowed';

    setTimeout(() => {
        objeto.removeAttribute('disabled');
        objeto.style.pointerEvents = '';
        objeto.style.opacity = '';
        objeto.style.cursor = '';
    }, duracion);
};
