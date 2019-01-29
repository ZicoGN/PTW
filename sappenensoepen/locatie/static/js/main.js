var markers = [];
var map;
var address;
// map inladen
function initMap() {
    counter =1;
    // map instellingen
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
                featureType: 'administrative.locality',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'poi',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'poi.park',
                elementType: 'geometry',
                stylers: [{color: '#263c3f'}]
            },
            {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{color: '#6b9a76'}]
            },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{color: '#38414e'}]
            },
            {
                featureType: 'road',
                elementType: 'geometry.stroke',
                stylers: [{color: '#212a37'}]
            },
            {
                featureType: 'road',
                elementType: 'labels.text.fill',
                stylers: [{color: '#9ca5b3'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry',
                stylers: [{color: '#746855'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry.stroke',
                stylers: [{color: '#1f2835'}]
            },
            {
                featureType: 'road.highway',
                elementType: 'labels.text.fill',
                stylers: [{color: '#f3d19c'}]
            },
            {
                featureType: 'transit',
                elementType: 'geometry',
                stylers: [{color: '#2f3948'}]
            },
            {
                featureType: 'transit.station',
                elementType: 'labels.text.fill',
                stylers: [{color: '#d59563'}]
            },
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{color: '#17263c'}]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.fill',
                stylers: [{color: '#515c6d'}]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.stroke',
                stylers: [{color: '#17263c'}]
            }
        ]
    });
    var stock = "Hoi";
    // om address te vertalen naar lan en lat
    var geocoder = new google.maps.Geocoder();
    geocodeAddress(address,geocoder,counter, false);
    // on sumbit click voer dit uit
    document.getElementById('submit').addEventListener('click', function () {
    
        // data van input veld
        var address = document.getElementById('location').value;
        // plaats marker
        geocodeAddress(address, geocoder,counter);
        // lijnen om stad heen
        places();
        counter += 1;
    })
}



// teken lijnen om stad heen
function drawCity(cityName) {
    $.ajax({
        dataType: "json",
        // json url met benodige geojson data
        url: 'https://nominatim.openstreetmap.org/search.php?q='+ cityName + '+Nederland&polygon_geojson=1&format=json&format=geojson',
        success: function (data) {
            addData = data.features[1];
            map.data.addGeoJson(addData);
            map.data.setStyle({
                fillColor: "Orange",
                strokeWeight: 1
            });
        }
    });
}
function getRandomColor() {
  var length = 6;
  var chars = '0123456789ABCDEF';
  var hex = '#';
  while(length--) hex += chars[(Math.random() * 16) | 0];
  return hex;
}

// DJANGO TO JAVASCRIPT
function places() {
    const arr = adreslist.split(",");;
    for (i = 0; i < arr.length; i++) { 
        drawCity(arr[i]);
        console.log(arr[i]);
}

}
// vertaald address naar lat en lan
function geocodeAddress(address,geocoder,counter, placeMarker = true) {
    // adress leeg dan standaard utrecht
    if (address == null) {
        address = 'Utrecht'
    }
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);


            // reset lijen om stad
            map.data.forEach(function(feature) {
                map.data.remove(feature);
            });

            // reset counter en markers
            deleteMarkers();


            if (placeMarker) {


                var contentString = '' + counter + '';
                addMarker(
                    {
                        location:results[0].geometry.location,
                        labelNumber: counter,
                        content: contentString
                    })
            }

        } else {
            
        }
    })
}

// voeg market toe aan maps
function addMarker(attr) {
    var marker = new google.maps.Marker({
        map: map,
        label: {text:'' + attr.labelNumber + '',color:'white'},
        position: attr.location
    });
    if(attr.content) {
        var infowindow = new google.maps.InfoWindow({
            content: attr.content
        });
        marker.addListener('click', function() {
            infowindow.open(map,marker);
        });
    }
    markers.push(marker)

}

// verwijder alle markers
function deleteMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

    markers = [];
    counter = 1;
}

var slider1 = document.getElementById('slider1');
var slider2 = document.getElementById('slider2');
var slider3 = document.getElementById('slider3');

noUiSlider.create(slider1, {
    start: [0, 1000],
    connect: true,
    range: {
        'min': 0,
        'max': 1000
    },
    tooltips:[true,true]

});

slider1.noUiSlider.on('change', function() {
    console.log(priceSlider.noUiSlider.get())
});

noUiSlider.create(slider2, {
    start: [0, 1000],
    connect: true,
    range: {
        'min': 0,
        'max': 1000
    },
    tooltips:[true,true]

});
slider2.noUiSlider.on('change', function() {
    console.log(priceSlider.noUiSlider.get())
});

noUiSlider.create(slider3, {
    start: [0, 1000],
    connect: true,
    range: {
        'min': 0,
        'max': 1000
    },
    tooltips:[true,true]

});
slider3.noUiSlider.on('change', function() {
    console.log(priceSlider.noUiSlider.get())
});