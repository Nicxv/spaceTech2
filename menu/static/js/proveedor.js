let map;
let marker;
let autocomplete;
let geocoder;

function initAutocomplete() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });

    marker = new google.maps.Marker({
        map: map,
        draggable: true
    });

    geocoder = new google.maps.Geocoder();

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        {types: ['geocode']}
    );

    autocomplete.addListener('place_changed', onPlaceChanged);

    map.addListener('click', (e) => {
        placeMarkerAndPanTo(e.latLng, map);
    });

    marker.addListener('dragend', (e) => {
        geocodePosition(marker.getPosition());
    });
}

function onPlaceChanged() {
    let place = autocomplete.getPlace();
    if (!place.geometry) {
        window.alert("No details available for input: '" + place.name + "'");
        return;
    }

    map.setCenter(place.geometry.location);
    map.setZoom(17);

    marker.setPosition(place.geometry.location);
    document.getElementById('direccion').value = place.formatted_address;
}

function placeMarkerAndPanTo(latLng, map) {
    marker.setPosition(latLng);
    map.panTo(latLng);
    geocodePosition(latLng);
}

function geocodePosition(pos) {
    geocoder.geocode({
        location: pos
    }, (results, status) => {
        if (status === 'OK') {
            if (results[0]) {
                document.getElementById('autocomplete').value = results[0].formatted_address;
            } else {
                window.alert('No results found');
            }
        } else {
            window.alert('Geocoder failed due to: ' + status);
        }
    });
}