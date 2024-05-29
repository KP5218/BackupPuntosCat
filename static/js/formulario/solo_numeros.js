//Desarrollado por Barbara Vera
const telefonoInput = document.getElementById('telefono');

telefonoInput.addEventListener('keypress', function(event) {
    const keyCode = event.keyCode;
    if (keyCode < 48 || keyCode > 57) {
        event.preventDefault();
    }
});
