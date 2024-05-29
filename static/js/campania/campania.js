//Desarrollado por Manuel Godoy
// variables
nombre_campania = document.getElementById("nombre_campania");
fecha_inicio = document.getElementById("fecha_inicio");
hora_inicio = document.getElementById("hora_inicio");
fecha_termino = document.getElementById("fecha_termino");
hora_termino = document.getElementById("hora_termino");
activo = document.getElementById("activo");
//
document.getElementById('submit_button').addEventListener('click', function(event) {
    formulario = document.getElementById("formulario_datos");
    if (!validar_campos()) {
        event.preventDefault();
        alert('Por favor, llene todos los campos requeridos.');
    } else{
        $.get("/reset/validacion_campania/" + fecha_inicio.value + "/" + fecha_termino.value + "/" + hora_inicio.value + "/" + hora_termino.value + "/", function(validador){
            if(validador.permitir == true){
                if(activo.checked){
                    $.get("/reset/campania_activa/", function(response){
                        if(response.campania_activa){
                             var respuesta = confirm("En este momento existe una campaña activa, si acepta seguir, la campaña actual se terminara ¿Seguro desea continuar?.");
                             if (respuesta == true){
                                 formulario.submit();
                             }else{
                                 alert("No se guardo ninguna campaña nueva...");
                             }
                        }else {
                        console.log("entre");
                             formulario.submit();
                        }
                    }).fail(function() {
                        alert('Error al verificar la campaña activa.');
                    });
                }else{
                    formulario.submit();
                }
            }else{
                alert("Las fechas de esta campaña se interponen con otras ya creadas...");
            }
        });
    }
});


function validar_campos(){
    let valido = true;

    const campos = [nombre_campania, fecha_inicio, hora_inicio, fecha_termino, hora_termino];

    campos.forEach(function(campo) {
        if (!campo.value.trim()) {
            valido = false;
            campo.style.borderColor = 'red';
        } else {
            campo.style.borderColor = '';
        }
    });

    return valido;
}