$(document).ready(function() {
    var selectElement = $('#select-campana');
    var errorMessage = $('#error-message');
    var botonEnviar = $('#boton-enviar');
    var formulario = $('#form');

    buscarCampana('');

    selectElement.change(function() {
        var nombre = $(this).val().trim();
        if (nombre !== '') {
            botonEnviar.prop('disabled', false);
        } else {
            botonEnviar.prop('disabled', true);
        }
    });

    function buscarCampana(nombre) {
        $.ajax({
            url: '/premio/buscar_campana/',
            data: { 'nombre': nombre },
            dataType: 'json',
            success: function(data) {
            console.log(data)
                if (data.length > 0) {
                    errorMessage.hide();
                    cargarOpciones(data);
                } else {
                    errorMessage.text('No se encontraron coincidencias con ninguna campaña.').show();
                    selectElement.empty().append('<option value="" selected disabled>Selecciona una campaña</option>');
                    botonEnviar.prop('disabled', true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error en la solicitud AJAX:", error);
            }
        });
    }

    function cargarOpciones(campanas) {
        selectElement.empty().append('<option value="" selected disabled>Selecciona una campaña</option>');
        campanas.forEach(function(campana) {
            selectElement.append('<option value="' + campana.nombre + '">' + campana.nombre + '</option>');
        });
    }

    formulario.submit(function(event) {
        event.preventDefault();

        $.ajax({
            url: formulario.attr('action'),
            type: formulario.attr('method'),
            data: formulario.serialize(),
            success: function(response) {
                if (response.success) {
                    window.location.href = "/premio/";
                } else {
                    errorMessage.text(response.error).show();
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});
