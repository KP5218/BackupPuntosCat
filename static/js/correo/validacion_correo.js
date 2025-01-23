function existerutcorreo() {
        var botonguardar = document.getElementById("boton-enviar");
        var rut = document.getElementById('rut').value;
        if (rut) {
            fetch(`/correo/existe_rut/${rut}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                if (data.length === 0) {
                    console.log("No se encontró el correo");
                    botonguardar.disabled = false;
                } else {
                        alert('el rut ya existe en el sistema');
                        botonguardar.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
            });
        }
    }
    document.getElementById('rut').addEventListener('blur', existerutcorreo);

   function existecorreo() {
        var botonguardar = document.getElementById("boton-enviar");
        var correo = document.getElementById('correo').value;
        if (correo) {
            fetch(`/correo/existe_correo/${correo}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                if (data.length === 0) {
                    console.log("No se encontró el correo");
                    botonguardar.disabled = false;
                } else {
                        alert('el correo ya existe en el sistema');
                        botonguardar.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
            });
        }
    }
        document.getElementById('correo').addEventListener('blur', existecorreo);