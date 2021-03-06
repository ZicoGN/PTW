var markers = [];
var map;
var address;
// map inladen
function initMap() {
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
    // om address te vertalen naar lan en lat
    var geocoder = new google.maps.Geocoder();
    geocodeAddress(address,geocoder,false);
    // on sumbit click voer dit uit
    document.getElementById('submit').addEventListener('click', function () {
    submitClicked();
    })
    document.getElementById('update').addEventListener('click', function () {
    updatedata();
    })
}


function updatedata() {
    alert("Wait until finished!")
    $.ajax({
            type:'POST',
            url:'update/',
            data:{
                update:"update",
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            //get return
            success: function(data) {
                alert(data)
            }
        });  
}

//Post value sliders to DJANGO and get return.
function submitClicked() {
    // Remove all marked locations
    map.data.forEach(function(feature) {
    map.data.remove(feature);
    });
        $.ajax({
            type:'POST',
            url:'search/',
            data:{
                slider1:JSON.stringify(slider1.noUiSlider.get()),
                slider2:JSON.stringify(slider2.noUiSlider.get()),
                slider3:JSON.stringify(slider3.noUiSlider.get()),
                slider4:JSON.stringify(slider4.noUiSlider.get()),
                slider5:JSON.stringify(slider5.noUiSlider.get()),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            //get return
            success: function(data) {
                if (data != ''){
                places(data);
                }
            }
        });   
}

// Markeer places
function places(list) {
    const arr = list.split(",");;
    for (i = 0; i < arr.length; i++) { 
        drawCity(arr[i], 0.6);
        console.log(arr[i]);
    }
}


// teken lijnen om stad heen
function drawCity(cityName, opp) {
    $.ajax({
        dataType: "json",
        // json url met benodige geojson data
        url: 'https://nominatim.openstreetmap.org/search.php?q='+ cityName + '+Nederland&polygon_geojson=1&format=json&format=geojson',
        success: function (data) {
            addData = data.features[1];
            map.data.addGeoJson(addData);
            map.data.setStyle({
                fillColor: "Orange",
                strokeWeight: 2,
                fillOpacity: opp
            });
        }
    });
}


// vertaald address naar lat en lan
function geocodeAddress(address,geocoder,placeMarker = true) {
    // adress leeg dan standaard utrecht
    if (address == null) {
        address = 'Utrecht'
    }
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            map.setCenter(results[0].geometry.location);
        } 
    })
}

//CREATE SLIDERS
var slider1 = document.getElementById('slider1');
var slider2 = document.getElementById('slider2');
var slider3 = document.getElementById('slider3');
var slider4 = document.getElementById('slider4');
var slider5 = document.getElementById('slider5');

noUiSlider.create(slider1, {
    start: [0, 350000],
    connect: true,
    range: {
        'min': 0,
        'max': 350000},
    tooltips:[true,true],});
noUiSlider.create(slider2, {
    start: [1, 94],
    connect: true,
    range: {
        'min': 1,
        'max': 94},
    tooltips:[true,true]});
noUiSlider.create(slider3, {
    start: [0, 1500],
    connect: true,
    range: {
        'min': 0,
        'max': 1500},
    tooltips:[true,true]});
noUiSlider.create(slider4, {
    start: [20, 50],
    connect: true,
    range: {
        'min': 25,
        'max': 50},
    tooltips:[true,true]});
noUiSlider.create(slider5, {
    start: [1, 25],
    connect: true,
    range: {
        'min': 1,
        'max': 25},
    tooltips:[true,true]});

//CHANGE SLIDERS
function val() {
    if (document.getElementById("select_id").value == 1)
{   slider1.noUiSlider.destroy()
    noUiSlider.create(slider1, {
    start: [0, 350000],
    connect: true,
    range: {
        'min': 0,
        'max': 350000},
    tooltips:[true,true],});}
if (document.getElementById("select_id").value == 2)
{   slider1.noUiSlider.destroy()
    noUiSlider.create(slider1, {
    start: [0, 50000],
    connect: true,
    range: {
        'min': 0,
        'max': 50000},
    tooltips:[true,true],});}
if (document.getElementById("select_id").value == 3)
{   slider1.noUiSlider.destroy()
    noUiSlider.create(slider1, {
    start: [0, 5000],
    connect: true,
    range: {
        'min': 0,
        'max': 5000},
    tooltips:[true,true],});}}