function hideThis() {
    var elem = document.getElementById("filter_options");
    if (elem.classList.contains("sidebar")) {
      elem.classList.remove("sidebar");
      elem.classList.add("hidden_bar");
    } else {
      elem.classList.remove("hidden_bar");
      elem.classList.add("sidebar");
    }
  }
  