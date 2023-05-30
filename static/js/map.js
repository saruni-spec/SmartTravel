// Function to initialize the map
function initMap() {
    // Create a new map instance
    var map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: -1.2833, lng: 36.8167}, // Set initial map center position
      zoom: 12 // Set initial zoom level
    });

    // Add a marker for the user's location
    var marker = new google.maps.Marker({
      position: {lat: -1.2833, lng: 36.8167}, // Set marker position
      map: map, // Specify the map instance
      title: 'User Location' // Set marker title (tooltip)
    });
  }

  // Call the initMap function when the page has finished loading
  window.onload = initMap;