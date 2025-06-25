// =============================
// ASIGNACIÓN DE BECAS - JS
// =============================

$(document).ready(function () {
    inicializarDropzone();
    // configurarPresupuestoConFormato();
    configurarSliders();
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
            fileInput.files = e.dataTransfer.files;
            mostrarNombreArchivo(fileInput.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            mostrarNombreArchivo(fileInput.files[0]);
        }
    });

    $('#processBtn').on('click', function () {
        const archivo = fileInput.files[0];
        const algoritmo = $('#algoritmo').val();

        if (!archivo) {
            mostrarAlerta("warning", "¡Archivo requerido!", "Por favor, selecciona o arrastra un archivo Excel.");
            return;
        }

        if (!algoritmo) {
            mostrarAlerta("warning", "¡Algoritmo no seleccionado!", "Selecciona el tipo de algoritmo antes de continuar.");
            return;
        }

        const extensionValida = archivo.name.endsWith('.xlsx');
        const tamanoMaximo = 10 * 1024 * 1024; // 10MB

        if (!extensionValida || archivo.size > tamanoMaximo) {
            mostrarAlerta("warning", "Archivo no válido", "Debe ser un archivo .xlsx y pesar menos de 10MB.");
            return;
        }

        enviarFormularioConFiltros(archivo, algoritmo);
    });

    /**
     * Muestra el nombre del archivo seleccionado debajo del dropzone.
     * @param {File} archivo 
     */
    function mostrarNombreArchivo(archivo) {
        fileNameContainer.style.display = 'block';
        fileNameText.textContent = archivo.name;
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

    fetch('/procesar-filtros', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log('Datos recibidos:', data);

        if (data.error) {
            mostrarAlerta("error", "Error", data.error);
            return;
        }

        // Mostrar secciones
        document.querySelectorAll('.modern-card').forEach(div => div.removeAttribute('hidden'));

        // Llenar tablas
        llenarTabla('tablaPostulantes', data.seleccionados);
        llenarTabla('tablaNoPostulantes', data.no_seleccionados);

        // Mostrar presupuesto
        document.getElementById('PresupuestoSobrante').value = data.presupuesto_sobrante;
    })
    .catch(error => {
        mostrarAlerta("error", "Error en el servidor", "No se pudo procesar la selección. Intenta más tarde.");
        console.error(error);
    });
}


/**
 * Crea una tabla de datos con DataTables.
 */

function llenarTabla(idTabla, lista) {
    const tabla = $(`#${idTabla}`);

    // Destruir instancia previa si existe
    if ($.fn.DataTable.isDataTable(tabla)) {
        tabla.DataTable().clear().destroy();
    }

    // Limpiar encabezado y cuerpo
    const thead = tabla.find('thead');
    const tbody = tabla.find('tbody');
    thead.empty();
    tbody.empty();

    if (lista.length === 0) {
        tbody.append('<tr><td colspan="10" class="text-center text-muted">Sin resultados</td></tr>');
        return;
    }

    // Crear encabezados desde la primera fila
    const columnas = Object.keys(lista[0]);
    const encabezadoHTML = columnas.map(col => `<th>${col.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</th>`).join('');
    thead.append(`<tr>${encabezadoHTML}</tr>`);

    // Crear filas del cuerpo
    lista.forEach(item => {
        const filaHTML = columnas.map(col => `<td>${item[col]}</td>`).join('');
        tbody.append(`<tr>${filaHTML}</tr>`);
    });

    // Inicializar DataTable
    tabla.DataTable({
        responsive: true,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json'
        },
        pageLength: 10,
        lengthChange: false,
        autoWidth: false,
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