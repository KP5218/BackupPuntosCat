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
                    document.getElementById('direccion').value = data[0].direccion;
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
   document.getElementById('direccion').value = '';
   document.getElementById('telefono').value = '';
   document.getElementById('email').value = '';
}

document.getElementById('rut').addEventListener('blur', cargarDatosCliente);


function existe_derivacion(rut) {
    let botonguardar = document.getElementById("enviar");
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