const nombre_usuario = document.getElementById("nombre_usuario")
const nombre = document.getElementById("nombre")
const apellido = document.getElementById("apellido")
const email = document.getElementById("email")
const tfno = document.getElementById("tfno")
const clave = document.getElementById("clave")
const confirmar_clave = document.getElementById("confirmar_clave")

const form = document.getElementById("form")
const parrafo = document.getElementById("warnings")

const regexNombreApellido = /^[a-zA-Z\s]+$/
const regexTelefono = /^\d{8}$/
const regexClave = /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/

form.addEventListener("submit", (e) => {
    let warnings = ""
    let entrar = false
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    parrafo.innerHTML = ""

    if (nombre_usuario.value.trim().length < 6) {
        warnings += `El nombre de usuario debe tener al menos 6 caracteres.<br>`
        entrar = true
    }

    if (!regexNombreApellido.test(nombre.value.trim())) {
        warnings += `El nombre no puede contener números ni caracteres especiales.<br>`
        entrar = true
    }

    if (!regexNombreApellido.test(apellido.value.trim())) {
        warnings += `El apellido no puede contener números ni caracteres especiales.<br>`
        entrar = true
    }

    if (!regexEmail.test(email.value)) {
        warnings += `El email no es válido.<br>`
        entrar = true
    }

    if (!regexTelefono.test(tfno.value)) {
        warnings += `El teléfono debe tener 8 dígitos.<br>`
        entrar = true
    }

    if (!regexClave.test(clave.value)) {
        warnings += `La contraseña debe tener al menos 8 caracteres, incluir una mayúscula y un número.<br>`
        entrar = true
    }

    if (clave.value !== confirmar_clave.value) {
        warnings += `Las contraseñas no coinciden.<br>`
        entrar = true
    }

    if (entrar) {
        e.preventDefault()
        parrafo.innerHTML = warnings
    }
})

// Función para manejar el mapa de Google Maps y geocodificar la dirección
let map
let marker
let autocomplete
let geocoder

function initAutocomplete() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -33.4372, lng: -70.6506 }, // Centro en Santiago, Chile
        zoom: 13,
        restriction: {
            country: ['cl'] // Restringir búsqueda a Chile
        }
    })

    marker = new google.maps.Marker({
        map: map,
        draggable: true
    })

    geocoder = new google.maps.Geocoder()

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        { types: ['geocode'] }
    )

    autocomplete.addListener('place_changed', onPlaceChanged)

    map.addListener('click', (e) => {
        placeMarkerAndPanTo(e.latLng, map)
    })

    marker.addListener('dragend', (e) => {
        geocodePosition(marker.getPosition())
    })
}

function onPlaceChanged() {
    let place = autocomplete.getPlace()
    if (!place.geometry) {
        window.alert("No details available for input: '" + place.name + "'")
        return
    }

    map.setCenter(place.geometry.location)
    map.setZoom(17)

    marker.setPosition(place.geometry.location)
    document.getElementById('direccion').value = place.formatted_address
}

function placeMarkerAndPanTo(latLng, map) {
    marker.setPosition(latLng)
    map.panTo(latLng)
    geocodePosition(latLng)
}

function geocodePosition(pos) {
    geocoder.geocode({
        location: pos
    }, (results, status) => {
        if (status === 'OK') {
            if (results[0]) {
                document.getElementById('autocomplete').value = results[0].formatted_address
            } else {
                window.alert('No results found')
            }
        } else {
            window.alert('Geocoder failed due to: ' + status)
        }
    })
}



        
        // Función para alternar visibilidad de contraseñas
        function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const icon = input.nextElementSibling.querySelector('i');
            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            } else {
                input.type = "password";
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            }
        }
   