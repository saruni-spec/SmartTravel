function trackUserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(showPosition);
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  console.log("Latitude: " + latitude + ", Longitude: " + longitude);

  // Get the CSRF token from the meta tag
  var csrfToken = document.querySelector('meta[name=csrf-token]').content;

  // Create a new FormData object
  var formData = new FormData();
  formData.append("latitude", latitude);
  formData.append("longitude", longitude);
  formData.append("csrf_token", csrfToken); // Include the CSRF token as a form field

  // Send the location data to the Flask route using axios
  axios({
    method: 'post',
    url: '/tracker/track',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(function (response) {
    console.log("Location sent successfully.");
  })
  .catch(function (error) {
    console.log("Error sending location:", error);
  });
}
window.onload = trackUserLocation;



