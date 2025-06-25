// =============================
// ASIGNACIÓN DE BECAS - JS
// =============================

$(document).ready(function () {
    inicializarDropzone();
    configurarPresupuestoConFormato();
    configurarSliders();
    const popoverTrigger = document.querySelector('#helpIcon');
    new bootstrap.Popover(popoverTrigger, {
        trigger: 'hover focus',
        placement: 'bottom',
        html: true
    });
});


// =============================
// FUNCIONES GENERALES
// =============================

/**
 * Muestra una alerta con ícono emoji y texto personalizado.
 * @param {string} icon tipo de icon a mostrar en el título.
 * @param {string} titulo Título de la alerta.
 * @param {string} mensaje Cuerpo del mensaje.
 */
function mostrarAlerta(icon, titulo, mensaje) {
    Swal.fire({
        icon: `${icon}`,
        title: `${titulo}`,
        text: mensaje,
        confirmButtonText: 'Aceptar'
    });
}

/**
 * Inicializa el área de carga de archivos y el botón de procesamiento.
 */
function inicializarDropzone() {
    const dropzoneArea = $('#fileUploadArea').get(0);
    const fileInput = $('#fileInput').get(0);
    const fileNameContainer = $('#fileName').get(0);
    const fileNameText = $('#fileNameText').get(0);
    const btnEliminarArchivo = $('#btnEliminarArchivo').get(0);

    dropzoneArea.addEventListener('click', () => fileInput.click());

    dropzoneArea.addEventListener('dragover', e => {
        e.preventDefault();
        dropzoneArea.classList.add('highlight');
    });

    dropzoneArea.addEventListener('dragleave', () => {
        dropzoneArea.classList.remove('highlight');
    });

    dropzoneArea.addEventListener('drop', e => {
        e.preventDefault();
        dropzoneArea.classList.remove('highlight');
        if (e.dataTransfer.files.length > 0) {
            const archivo = e.dataTransfer.files[0];
            if (validarArchivo(archivo)) {
                fileInput.files = e.dataTransfer.files;
                mostrarNombreArchivo(archivo);
            }
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const archivo = fileInput.files[0];
            if (validarArchivo(archivo)) {
                mostrarNombreArchivo(archivo);
            } else {
                fileInput.value = ''; // Limpiar input si no es válido
                fileNameContainer.style.display = 'none';
            }
        }
    });

  btnEliminarArchivo.addEventListener('click', limpiarArchivo);

    function limpiarArchivo() {
        fileInput.value = '';
        fileNameContainer.style.display = 'none';
        btnEliminarArchivo.classList.add('d-none');
        fileNameText.textContent = '';
    }

    $('#processBtn').on('click', function () {
        const archivo = fileInput.files[0];
        const algoritmo = $('#algoritmo').val();
        const presupuesto = $('#Presupuesto').val();
        const monto_requerido = $('#monto_requerido').val();

        if (!archivo) {
            mostrarAlerta("warning", "¡Archivo requerido!", "Por favor, selecciona o arrastra un archivo Excel.");
            return;
        }

        if (!algoritmo) {
            mostrarAlerta("warning", "¡Algoritmo no seleccionado!", "Selecciona el tipo de algoritmo antes de continuar.");
            return;
        }

        if (!presupuesto) {
            mostrarAlerta("warning", "Presupuesto no establecido!", "Debes colocar el presupuesto antes de procesar la información.");
            return;
        }

        if (!monto_requerido) {
            mostrarAlerta("warning", "Monto requerido no seleccionado!", "Debes colocar el tipo de monto requerido que se usará para la priorización.");
            return;
        }


        enviarFormularioConFiltros(archivo, algoritmo);
    });

    /**
     * Valida la extensión y tamaño del archivo.
     * @param {File} archivo
     * @returns {boolean} true si es válido, false si no lo es
     */
    function validarArchivo(archivo) {
        const extensionValida = archivo.name.endsWith('.xlsx');
        const tamanoMaximo = 10 * 1024 * 1024; // 10MB

        if (!extensionValida) {
            mostrarAlerta("warning", "Archivo no válido", "Debe ser un archivo con extensión: .xlsx");
            return false;
        }

        if (archivo.size > tamanoMaximo) {
            mostrarAlerta("warning", "Archivo demasiado grande", "El archivo debe pesar menos de 10MB.");
            return false;
        }

        return true;
    }

    /**
     * Muestra el nombre del archivo seleccionado debajo del dropzone.
     * @param {File} archivo 
     */
    function mostrarNombreArchivo(archivo) {
        fileNameContainer.style.display = 'block';
        fileNameText.textContent = archivo.name;
        btnEliminarArchivo.classList.remove('d-none');
    }
}


/**
 * Envia los datos al backend.
 * Agrupa los inputs en el form data para que tome los filtros, 
 * el tipo de algoritmo a usar y el archivo cargado.
 */

function enviarFormularioConFiltros(archivoExcel, algoritmo) {
    const form = $('#formFiltros')[0];
    const formData = new FormData(form);

    formData.append('archivo', archivoExcel);
    formData.append('algoritmo', algoritmo);

    // Si las secciones están visibles, ocultarlas
    const seccionesVisibles = Array.from(document.querySelectorAll('.modern-card'))
        .some(div => !div.hasAttribute('hidden'));
    
    if (seccionesVisibles) {
        ocultarSeccionesResultado();
    }

    $('#spinnerCarga').show();

    fetch('/procesar-filtros', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        $('#spinnerCarga').hide();

        if (data.error) {
            mostrarAlerta("error", "Error", data.error);
            return;
        }

        llenarTabla('tablaPostulantes', data.seleccionados);
        llenarTabla('tablaNoPostulantes', data.no_seleccionados);
        mostrarSeccionesResultado();

        document.getElementById('PresupuestoInvertido').value = data.presupuesto_invertido;
        document.getElementById('PresupuestoSobrante').value = data.presupuesto_sobrante;
    })
    .catch(error => {
        $('#spinnerCarga').hide();
        mostrarAlerta("error", "Error en el servidor", "No se pudo procesar la selección. Intenta más tarde.");
        console.error(error);
    });
}


function ocultarSeccionesResultado() {
    document.querySelectorAll('.cardDinamico').forEach(div => div.setAttribute('hidden', true));
}

function mostrarSeccionesResultado() {
    document.querySelectorAll('.cardDinamico').forEach(div => div.removeAttribute('hidden'));
}



/**
 * Crea una tabla de datos con DataTables.
 */
function llenarTabla(idTabla, lista) {
    const tabla = $(`#${idTabla}`);
    if ($.fn.DataTable.isDataTable(tabla)) {
        tabla.DataTable().clear().destroy();
    }

    const thead = tabla.find('thead');
    const tbody = tabla.find('tbody');
    thead.empty();
    tbody.empty();

    if (lista.length === 0) {
        tbody.append('<tr><td colspan="7" class="text-center text-muted">Sin resultados</td></tr>');
        return;
    }

    // Columnas deseadas, incluyendo la ocupación con badge
    const columnas = [
        { key: 'prioridad', label: 'Prioridad (1-8)' },
        { key: 'nombre', label: 'Nombre' },
        { key: 'genero', label: 'Género' },
        { key: 'nivel_socioeconomico', label: 'Nivel Socioeconómico' },
        { key: 'ocupacion', label: 'Ocupación' },
        { key: 'indice', label: 'Índice' },
        { key: 'monto_requerido', label: 'Monto Requerido' }        
    ];

    // Función para aplicar clase según tipo de ocupación
    function obtenerBadgePorOcupacion(tipo) {
        switch ((tipo || '').toUpperCase()) {
            case 'ESTUDIANTE': return '<span class="badge badge-gradient-estudiante fs-6">Estudiante</span>';
            case 'EMPLEADO': return '<span class="badge badge-gradient-empleado fs-6">Empleado</span>';
            case 'DESEMPLEADO': return '<span class="badge badge-gradient-desempleado fs-6">Desempleado</span>';
            case 'TRABAJO LIBRE': return '<span class="badge badge-gradient-trabajo-libre fs-6">Trabajo Libre</span>';
            default: return tipo || '-';
        }
    }

    // Encabezados
    const encabezadoHTML = columnas.map(c => `<th>${c.label}</th>`).join('');
    thead.append(`<tr>${encabezadoHTML}</tr>`);

    // Filas
    lista.forEach(item => {
        const filaHTML = columnas.map(col => {
            let valor = item[col.key];

            if (col.key === 'nombre') {
                valor = valor.toUpperCase();
            }

            if (col.key === 'ocupacion') {
                valor = obtenerBadgePorOcupacion(valor);
            }

            return `<td>${valor}</td>`;
        }).join('');
        tbody.append(`<tr>${filaHTML}</tr>`);
    });

    tabla.DataTable({
        responsive: true,
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json"
        },
        order: []
    });
}



/**
 * Aplica formato con comas al campo de presupuesto.
 */
function configurarPresupuestoConFormato() {
    $('#Presupuesto').on('input', function () {
        let posicionCursor = this.selectionStart;
        let longitudOriginal = this.value.length;

        let valorLimpio = this.value.replace(/[^\d.]/g, '');
        let valorFormateado = formatearConComas(valorLimpio);

        this.value = valorFormateado;

        let nuevaLongitud = valorFormateado.length;
        this.setSelectionRange(
            posicionCursor + (nuevaLongitud - longitudOriginal),
            posicionCursor + (nuevaLongitud - longitudOriginal)
        );
    });

    function formatearConComas(valor) {
        valor = valor.replace(/,/g, '');
        let [parteEntera, parteDecimal] = valor.split(".");
        parteEntera = parteEntera.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        if (parteDecimal !== undefined) {
            parteDecimal = parteDecimal.substring(0, 3);
            return `${parteEntera}.${parteDecimal}`;
        }
        return parteEntera;
    }
}


/**
 * Configura los sliders de edad e índice y actualiza los valores en inputs ocultos.
 */
function configurarSliders() {
    const edadSlider = $('#edadSlider').get(0);
    const indiceSlider = $('#indiceSlider').get(0);

    noUiSlider.create(edadSlider, {
        start: [10, 70],
        connect: true,
        step: 1,
        range: { min: 10, max: 70 },
        format: {
            to: value => Math.round(value),
            from: value => Number(value)
        }
    });

    noUiSlider.create(indiceSlider, {
        start: [0, 100],
        connect: true,
        step: 1,
        range: { min: 0, max: 100 },
        format: {
            to: value => Math.round(value),
            from: value => Number(value)
        }
    });

    const edadMin = $('#edadMin');
    const edadMax = $('#edadMax');
    const indiceMin = $('#indiceMin');
    const indiceMax = $('#indiceMax');

    const inputEdadMin = $('#inputEdadMin');
    const inputEdadMax = $('#inputEdadMax');
    const inputIndiceMin = $('#inputIndiceMin');
    const inputIndiceMax = $('#inputIndiceMax');

    edadSlider.noUiSlider.on('update', function (values) {
        edadMin.text(values[0]);
        edadMax.text(values[1]);
        inputEdadMin.val(values[0]);
        inputEdadMax.val(values[1]);
    });

    indiceSlider.noUiSlider.on('update', function (values) {
        indiceMin.text(values[0]);
        indiceMax.text(values[1]);
        inputIndiceMin.val(values[0]);
        inputIndiceMax.val(values[1]);
    });
}