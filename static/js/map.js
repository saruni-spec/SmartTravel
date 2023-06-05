// Initialize the map
function initMap() {
  // Create a new map centered at a default location
  console.log('map')
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 1.2921, lng: 36.8219 }, // Default location (Nairobi)
    
  });

  // Try to get the user's current location
  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      (position) => {
        const { latitude, longitude } = position.coords;

        // Center the map on the user's current location
        map.setCenter({ lat: latitude, lng: longitude });

        // Create a marker to indicate the user's location
        const marker = new google.maps.Marker({
          position: { lat: latitude, lng: longitude },
          map: map,
          title: "You are here",
        });
      },
      (error) => {
        console.error("Error getting user location:", error);
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
  }
}

window.onload = initMap;