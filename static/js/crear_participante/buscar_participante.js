   function existerut() {
        var botonguardar = document.getElementById("enviar");
        var rut = document.getElementById('rut').value;
        if (rut) {
            fetch(`/participante/existe_participante/${rut}`)
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
                    botonguardar.disabled = false;
                } else {
                        alert('el rut ya existe en la bd');
                        botonguardar.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
            });
        }
    }
    document.getElementById('rut').addEventListener('blur', existerut);



       function existeusuario() {
        var botonguardar = document.getElementById("enviar");
        var usuario = document.getElementById('usuario').value;
        if (usuario) {
            fetch(`/participante/existe_usuario/${usuario}`)
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
                    botonguardar.disabled = false;
                } else {
                        alert('el usuario ya existe en la bd');
                        botonguardar.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error al obtener datos del cliente:', error);
            });
        }
    }
    document.getElementById('usuario').addEventListener('blur', existeusuario);