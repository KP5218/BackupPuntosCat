   function cargarDatosCliente() {
        var rut = document.getElementById('rut').value;
        var divObservacion = document.getElementById('div_observacion');
        var textareaObservacion = document.getElementById('observacion');
        if (rut) {
            fetch(`/base_cliente/${rut}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                if (data.length === 0) {
                    console.log("No se encontró al cliente");
                    divObservacion.style.display = 'none';
                    textareaObservacion.required = false;
                    limpiarCamposFormulario();
                     existe_derivacion(rut);
                } else {
                    document.getElementById('nombre').value = data[0].nombre + " " + data[0].appaterno + " " + data[0].apmaterno;
                    document.getElementById('telefono').value = data[0].fonomovil;
                    document.getElementById('email').value = data[0].email;

                    divObservacion.style.display = 'none';
                    textareaObservacion.required = false;

                    existe_derivacion(rut);
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
                limpiarCamposFormulario();
            });
        }
    }

function limpiarCamposFormulario() {
   document.getElementById('nombre').value = '';
   document.getElementById('telefono').value = '';
   document.getElementById('email').value = '';
}




function existe_derivacion(rut) {
    var botonguardar = document.getElementById("enviar");
    if (rut) {
        fetch(`/busqueda/${rut}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                var divObservacion = document.getElementById('div_observacion');
                var textareaObservacion = document.getElementById('observacion');
                if (data.length === 0) {
                    console.log("No se encontró el dato");
                    botonguardar.disabled = false;

                } else {
                    console.log("Se encontró el dato");

                    if(data[0].cantidad_derivacion <2){

                        divObservacion.style.display = 'block';
                        textareaObservacion.required = true;
                        alert("El cliente ya ha sido derivado anteriormente, si desea volver a derivarlo debe otorgar una razón");
                        botonguardar.disabled = false;
                    }else{
                        alert("El cliente ya ha superado el maximo de derivaciones");
                        botonguardar.disabled = true;
                    }
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
            });
    }
}

function cliente_rechazo() {
     var rut = document.getElementById('rut').value;
     var botonguardar = document.getElementById("enviar");
     if (rut) {
         fetch(`/cliente_rechazo/${rut}`)
         .then(response => {
             if (!response.ok) {
                 throw new Error('Error en la solicitud');
             }
             return response.json();
         })
         .then(data => {
             console.log(data);
             if (data.length === 0) {
                botonguardar.disabled = false;
                cargarDatosCliente();
                 limpiarCamposFormulario();

             } else {
                   alert("El cliente ha manifestado su intención de no adquirir el seguro.");
                   botonguardar.disabled = true;
             }
         })
         .catch(error => {
             console.error('Error al obtener datos del cliente:', error);
             limpiarCamposFormulario();
         });
     }
}

document.getElementById('rut').addEventListener('blur', cliente_rechazo);



function fonoRequired() {
       var telefonoInput = document.getElementById('telefono');
       var rechazaSeguroCheckbox = document.getElementById('rechaza_seguro');
       if (rechazaSeguroCheckbox.checked) {
           telefonoInput.removeAttribute('required');
       } else {
           telefonoInput.setAttribute('required', 'required');
       }
}
document.getElementById('rechaza_seguro').addEventListener('change', fonoRequired);