document.addEventListener("DOMContentLoaded", function() {

});

function mostrarTipobusqueda() {
    var tipoBusqueda = document.getElementById('busqueda2').value;
    var tipoEleccion = document.getElementById('eleccion').value;
    var inputCampania = document.getElementById('campanaInput');
    var selectCampania = document.getElementById('campana-select');
    var tabladetalle = document.getElementById('detalle-campana');
    var errorMessageDiv = document.getElementById('error-message1');

    document.getElementById('fechaInicio').value = '';
    document.getElementById('fechaFin').value = '';
    selectCampania.value = '';

    if (tipoBusqueda == 'campana' && tipoEleccion == 'campana') {
        inputCampania.style.display = 'block';
        selectCampania.setAttribute('required', 'required');
        errorMessageDiv.style.display = 'none';
    } else {
        inputCampania.style.display = 'none';
        tabladetalle.style.display = 'none';
        selectCampania.removeAttribute('required');
    }
}


function mostrarFechas() {
    var divfecha = document.getElementById('fechas');
    var fechaInicio = document.getElementById('fechaInicio');
    var fechaFinal = document.getElementById('fechaFin');
    var tipoEleccion = document.getElementById('eleccion').value;
    var tipoBusqueda = document.getElementById('busqueda2').value;
    var divBusqueda = document.getElementById('busqueda');
    var inputCampania = document.getElementById('campanaInput');
    var selectCampania = document.getElementById('campana-select');
    var tabladetalle = document.getElementById('detalle-campana');
    var clienteOption = document.querySelector('#busqueda2 option[value="Cliente"]');
    var derivacionOption = document.querySelector('#busqueda2 option[value="derivacion"]');
    var puntajeOption = document.querySelector('#busqueda2 option[value="puntaje"]');
    var errorMessageDiv = document.getElementById('error-message1');

    selectCampania.value = '';

    if (tipoEleccion == 'fecha') {
        divBusqueda.style.display = 'block';
        divfecha.style.display = 'block';
        inputCampania.style.display = 'none';
        fechaInicio.setAttribute('required', 'required');
        fechaFinal.setAttribute('required', 'required');
        selectCampania.removeAttribute('required');

        clienteOption.style.display = 'none';
        derivacionOption.style.display = 'block';
        puntajeOption.style.display = 'block';

        errorMessageDiv.style.display = 'block';
    } else if (tipoEleccion == 'campana') {
        divBusqueda.style.display = 'block';
        divfecha.style.display = 'none';
        tabladetalle.style.display = 'none';
        fechaInicio.removeAttribute('required');
        fechaFinal.removeAttribute('required');

        clienteOption.style.display = 'block';
        derivacionOption.style.display = 'none';
        puntajeOption.style.display = 'none';

        errorMessageDiv.style.display = 'none';
    } else {
        divBusqueda.style.display = 'none';
        divfecha.style.display = 'none';
        tabladetalle.style.display = 'none';
        fechaInicio.removeAttribute('required');
        fechaFinal.removeAttribute('required');

        errorMessageDiv.style.display = 'none';
    }

    if (tipoBusqueda == 'campana' && tipoEleccion == 'campana') {
        inputCampania.style.display = 'block';
        selectCampania.setAttribute('required', 'required');
    } else {
        inputCampania.style.display = 'none';
        tabladetalle.style.display = 'none';
        selectCampania.removeAttribute('required');
    }
}


function validarFechas() {
    var fechaRegex = /^\d{4}-\d{2}-\d{2}$/;

    var fechaInicio = document.getElementById("fechaInicio").value;
    var fechaFin = document.getElementById("fechaFin").value;
    var errorMessage = document.getElementById("error-message1");
    if (!fechaRegex.test(fechaInicio) || !fechaRegex.test(fechaFin)) {
        errorMessage.innerText = "Por favor ingresa fechas válidas en el formato YYYY-MM-DD.";
        return false;
    }

    if (fechaInicio > fechaFin) {
        errorMessage.innerText = "La fecha de inicio no puede ser posterior a la fecha de fin.";
        return false;
    }

    errorMessage.innerText = "";
    return true;
}

function formatearFecha(fecha)
{
var fechaObj = new Date(fecha);
var dia = String(fechaObj.getDate()).padStart(2, '0');
var mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
var anio = fechaObj.getFullYear();
return dia + '-' + mes + '-' + anio;
}


$(document).ready(function() {
    var selectElement = $('#campana-select');
    var errorMessage2 = $('#error-message2');
    var campaniaValida = false;

    selectElement.on('change', function() {
        var nombre = $(this).val().trim();
        errorMessage2.hide();
        if (nombre !== '') {
            obtenerDetallesCampana(nombre);
        } else {
            campaniaValida = false;
        }
    });

    function obtenerDetallesCampana(nombre) {
        $.ajax({
            url: 'buscar_detalles_campana/',
            data: {
                nombre: nombre
            },
            dataType: 'json',
            success: function(data) {
                if (!data.error) {
                    mostrarDetallesCampana(data);
                    campaniaValida = true;
                } else {
                    errorMessage2.text(data.error).show();
                    campaniaValida = false;
                }
            }
        });
    }

    function mostrarDetallesCampana(detalles) {
        $('#detalle-nombre').text(detalles.nombre);
        $('#detalle-fecha-inicio').text(formatearFecha(detalles.fecha_inicio));
        $('#detalle-fecha-fin').text(formatearFecha(detalles.fecha_fin));

        $('#detalle-campana').show();
    }

    function cargarCampanas() {
        $.ajax({
            url: 'buscar_campana/',
            dataType: 'json',
            success: function(data) {
                if (data.length > 0) {
                    errorMessage2.hide();
                    mostrarOpciones(data);
                } else {
                    errorMessage2.text('No se encontraron campañas disponibles.').show();
                }
            }
        });
    }

    function mostrarOpciones(campanas) {
        campanas.sort(function(a, b) {
            return a.nombre.localeCompare(b.nombre);
        });

        selectElement.empty();
        selectElement.append('<option value="">Seleccione una campaña</option>');

        campanas.forEach(function(campana) {
            selectElement.append('<option value="' + campana.nombre + '">' + campana.nombre + '</option>');
        });
    }

    $('#Formulario').on('submit', function(event) {
        var valido = true;
        if (selectElement.attr('required') && !campaniaValida) {
            valido = false;
            alert('Por favor, seleccione una campaña válida.');
        }
        if ($('#fechaInicio').attr('required') && !validarFechas()) {
            valido = false;
        }
        if (!valido) {
            event.preventDefault();
        }
    });

    cargarCampanas();
});



document.getElementById('campana-select').addEventListener('change', function() {
    var selectedOption = this.options[this.selectedIndex].text;
    document.getElementById('nombre-campania').value = selectedOption;
});