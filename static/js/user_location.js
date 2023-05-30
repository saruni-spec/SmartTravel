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

  // Send the location data to the Flask route using fetch API
  fetch('/profile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ latitude: latitude, longitude: longitude }),
  })
    .then(function (response) {
      if (response.ok) {
        console.log("Location sent successfully.");
      } else {
        console.log("Error sending location.");
      }
    })
    .catch(function (error) {
      console.log("An error occurred:", error);
    });
}


