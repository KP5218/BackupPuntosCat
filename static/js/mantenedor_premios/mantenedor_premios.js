$(document).ready(function() {
    function mostrarPremios() {
        $.ajax({
            url: '/mostrar_premio/',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                $('#user-list').empty();
                if (response && response.premios && Array.isArray(response.premios)) {
                    var contador = 1;
                    response.premios.forEach(function(premio) {
                        $('#user-list').append('<li class="list-group-item">' + contador + '. ' + premio + '</li>');
                        contador++;
                    });
                } else {
                    console.error('Propiedad premios inválida ', response);
                }
            }
        });
    }

    $('#modal-premios').on('shown.bs.modal', function() {
        mostrarPremios();
    });
});
