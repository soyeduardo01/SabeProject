$(document).ready(function () {
    const columnas = ["NOMBRE", "GÉNERO", "NIVEL SOCIOECONÓMICO", "OCUPACIÓN", "ÍNDICE", "MONTO REQUERIDO"];
    const datos = [
        ["ANA GÓMEZ", "FEMENINO", "BAJO", "ESTUDIANTE", 91.5, "RD$450,000"],
        ["JUAN PÉREZ", "MASCULINO", "MEDIO", "EMPLEADO", 88.2, "RD$410,000"],
        ["LUCÍA MARTÍNEZ", "FEMENINO", "MEDIO-ALTO", "TRABAJO LIBRE", 93.0, "RD$460,000"],
        ["MIGUEL HERRERA", "MASCULINO", "MEDIO-BAJO", "DESEMPLEADO", 87.6, "RD$430,000"],
        ["CARLA RAMOS", "FEMENINO", "ALTO", "ESTUDIANTE", 89.9, "RD$470,000"],
        ["ENRIQUE LÓPEZ", "MASCULINO", "MEDIO", "EMPLEADO", 90.0, "RD$500,000"],
        ["SOFÍA MEJÍA", "FEMENINO", "BAJO", "ESTUDIANTE", 92.3, "RD$480,000"],
        ["JOSÉ RAMÍREZ", "MASCULINO", "MEDIO", "DESEMPLEADO", 85.1, "RD$420,000"],
        ["PAULA ROSARIO", "FEMENINO", "MEDIO-ALTO", "TRABAJO LIBRE", 94.4, "RD$530,000"],
        ["ALBERTO CASTILLO", "MASCULINO", "MEDIO-BAJO", "EMPLEADO", 89.0, "RD$445,000"],
        ["ANDREA TEJADA", "FEMENINO", "ALTO", "ESTUDIANTE", 90.7, "RD$490,000"],
        ["FRANCISCO NUÑEZ", "MASCULINO", "BAJO", "DESEMPLEADO", 86.5, "RD$440,000"],
        ["GABRIELA INFANTE", "FEMENINO", "MEDIO", "EMPLEADO", 92.9, "RD$510,000"],
        ["RAFAEL TAVERAS", "MASCULINO", "MEDIO-ALTO", "TRABAJO LIBRE", 88.8, "RD$460,000"],
        ["ISABEL MEDINA", "FEMENINO", "MEDIO", "ESTUDIANTE", 91.2, "RD$470,000"]
    ];

    const $table = $('#tablaPostulantes');
    const $thead = $table.find('thead');
    const $tbody = $table.find('tbody');

    if ($.fn.DataTable.isDataTable($table)) {
        $table.DataTable().destroy();
    }

    $thead.empty().append('<tr></tr>');
    const $theadRow = $thead.find('tr');

    $.each(columnas, function (_, col) {
        $('<th>', {
            text: col,
            class: 'text-center'
        }).appendTo($theadRow);
    });

    $tbody.empty();
    $.each(datos, function (_, row) {
        const $tr = $('<tr>');
        $.each(row, function (index, cell) {
            const $td = $('<td>').addClass('text-center');
            if (index === 3) {
                const clase = {
                    "ESTUDIANTE": "badge-gradient-estudiante",
                    "EMPLEADO": "badge-gradient-empleado",
                    "DESEMPLEADO": "badge-gradient-desempleado",
                    "TRABAJO LIBRE": "badge-gradient-trabajo-libre"
                }[cell] || "";
                $('<span>', {
                    text: cell,
                    class: 'badge ' + clase
                }).appendTo($td);
            } else {
                $td.text(cell);
            }
            $tr.append($td);
        });
        $tbody.append($tr);
    });

    $table.DataTable({
        responsive: true,
        columnDefs: [{
            targets: 4,
            type: 'num'
        }],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json"
        },
        pageLength: 10
    });

    // Sliders
    const edadSlider = $('#edadSlider');
    const indiceSlider = $('indiceSlider');

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

    const $edadMin = $('#edadMin');
    const $edadMax = $('#edadMax');
    const $indiceMin = $('#indiceMin');
    const $indiceMax = $('#indiceMax');

    // Referencias a los input hidden
    const $inputEdadMin = $('#inputEdadMin');
    const $inputEdadMax = $('#inputEdadMax');
    const $inputIndiceMin = $('#inputIndiceMin');
    const $inputIndiceMax = $('#inputIndiceMax');

    edadSlider.noUiSlider.on('update', function (values) {
        $edadMin.text(values[0]);
        $edadMax.text(values[1]);
        $inputEdadMin.val(values[0]);
        $inputEdadMax.val(values[1]);
    });

    indiceSlider.noUiSlider.on('update', function (values) {
        $indiceMin.text(values[0]);
        $indiceMax.text(values[1]);
        $inputIndiceMin.val(values[0]);
        $inputIndiceMax.val(values[1]);
    });
});

// BOTÓN: PROCESAR FILTROS DE PRIORIDAD.

$('#processBtn').on('click', function (e) {
    e.preventDefault(); // evita que recargue si es necesario hacer validaciones

    // Puedes hacer validaciones aquí si quieres

    $('#formFiltros').submit(); // envía el formulario al backend
});
