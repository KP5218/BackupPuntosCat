document.addEventListener("DOMContentLoaded", function() {
    mostrarEntradas();
});

function mostrarEntradas() {
    var opcionSeleccionada = document.getElementById("busqueda").value;

    if (opcionSeleccionada === "codigo1") {
        document.getElementById("busquedafecha").closest('th').style.display = 'table-cell';
    } else if (opcionSeleccionada === "codigo2") {
        document.getElementById("busquedafecha").closest('th').style.display = 'table-cell';
    }
}



function validarFechas() {
        var fechaInicio = document.getElementById("fechaInicio").value;
        var fechaFin = document.getElementById("fechaFin").value;

        if (fechaInicio > fechaFin) {
            document.getElementById("error-message").innerHTML = "La fecha de inicio no puede ser posterior a la fecha de fin.";
            return false;
        } else {
            document.getElementById("error-message").innerHTML = "";
        }
        return true;
    }