document.addEventListener('DOMContentLoaded', function () {
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

    const tableId = '#tablaPostulantes';
    const thead = document.querySelector(`${tableId} thead`);
    const tbody = document.querySelector(`${tableId} tbody`);

    if ($.fn.DataTable.isDataTable(tableId)) {
        $(tableId).DataTable().destroy();
    }

    thead.innerHTML = '<tr></tr>';
    tbody.innerHTML = '';

    const theadRow = thead.querySelector('tr');
    columnas.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        th.classList.add('text-center');
        theadRow.appendChild(th);
    });

    datos.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach((cell, index) => {
            const td = document.createElement('td');
            td.classList.add('text-center');

            if (index === 3) { // OCUPACIÓN
                const span = document.createElement('span');
                span.textContent = cell;

                const clase = {
                    "ESTUDIANTE": "badge-gradient-estudiante",
                    "EMPLEADO": "badge-gradient-empleado",
                    "DESEMPLEADO": "badge-gradient-desempleado",
                    "TRABAJO LIBRE": "badge-gradient-trabajo-libre"
                }[cell] || "";

                span.classList.add('badge', clase);
                td.appendChild(span);
            } else {
                td.textContent = cell;
            }

            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });

    $(tableId).DataTable({
        responsive: true,
        columnDefs: [
        {
            targets: 4, // Índice está en la columna 4 (comenzando desde 0)
            type: 'num' // asegúrate que sea tratada como número
        }
        ],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json"
        },
        pageLength: 10
    });


  
  const edadSlider = document.getElementById('edadSlider');
  const indiceSlider = document.getElementById('indiceSlider');

  noUiSlider.create(edadSlider, {
    start: [10, 70], 
    connect: true,
    step: 1,
    range: {
      'min': 10,
      'max': 70
    },
    format: {
      to: value => Math.round(value),
      from: value => Number(value)
    }
  });

  const edadMin = document.getElementById('edadMin');
  const edadMax = document.getElementById('edadMax');

  edadSlider.noUiSlider.on('update', (values) => {
    edadMin.textContent = values[0];
    edadMax.textContent = values[1];
  });

  noUiSlider.create(indiceSlider, {
    start: [0, 100], 
    connect: true,
    step: 1,
    range: {
      'min': 0,
      'max': 100
    },
    format: {
      to: value => Math.round(value),
      from: value => Number(value)
    }
  });

  const indiceMin = document.getElementById('indiceMin');
  const indiceMax = document.getElementById('indiceMax');

  indiceSlider.noUiSlider.on('update', (values) => {
    indiceMin.textContent = values[0];
    indiceMax.textContent = values[1];
  });

});
