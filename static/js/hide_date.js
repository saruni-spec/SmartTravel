function hideDates() {
    var elem = document.getElementById("date_options");
    if (elem.classList.contains("date_filter")) {
      elem.classList.remove("date_filter");
      elem.classList.add("date_hide");
    } else {
      elem.classList.remove("date_hide");
      elem.classList.add("date_filter");
    }
  }
  