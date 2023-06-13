window.onload = function() {
  // Get the user_location data from the Flask view function
  var user_location = {{ user_location|tojson }};
  console.log(user_location);
  var latitude = user_location.latitude;
  console.log(latitude)
  var longitude = user_location.longitude;

  // The location of the place
  var location = { latitude, longitude };
  console.log(location);
  // The map, centered at the location
  var map = new google.maps.Map(
    document.getElementById('map'), { zoom: 4, center: location });
  // The marker, positioned at the location
  var marker = new google.maps.Marker({ position: location, map: map });
};