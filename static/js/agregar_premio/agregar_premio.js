$(document).ready(function() {
    var inputElement = $('#autocomplete-input');
    var suggestionsList = $('#resultados');
    var errorMessage = $('#error-message');
    var botonEnviar = $('#boton-enviar');

    inputElement.on('input', function() {
        var nombre = $(this).val().trim();
        if (nombre !== '') {
            buscarCampana(nombre);
        } else {
            suggestionsList.empty().hide();
            botonEnviar.prop('disabled', true);
        }
    });

    function buscarCampana(nombre) {
        $.ajax({
            url: '/premio/buscar_campana/',
            data: {
                'nombre': nombre
            },
            dataType: 'json',
            success: function(data) {
                if (data.length > 0) {
                    errorMessage.hide();
                    mostrarResultados(data);
                    botonEnviar.prop('disabled', false);
                } else {
                    errorMessage.text('No se encontraron coincidencias con ninguna campaña.').show();
                    botonEnviar.prop('disabled', true);
                }
            }
        });
    }

    function mostrarResultados(resultados) {
        suggestionsList.empty();
        resultados.forEach(function(campana) {
            suggestionsList.append('<a href="#" class="list-group-item list-group-item-action">' + campana.nombre + '</a>');
        });
        suggestionsList.show();
    }

    suggestionsList.on('click', 'a', function() {
        inputElement.val($(this).text());
        suggestionsList.empty().hide();
        botonEnviar.prop('disabled', false);
    });

    formulario.submit(function(event) {
        event.preventDefault();

    });
});
