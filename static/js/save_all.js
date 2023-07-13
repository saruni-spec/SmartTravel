function downloadFormsAsDoc() {
  var doc = new jsPDF();
  var yPos = 20;

  // Get all the forms on the page excluding date_filter and sidebar
  var forms = document.querySelectorAll("form:not(.date_filter):not(.sidebar)");

  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];
    var elements = form.elements;

    for (var j = 0; j < elements.length; j++) {
      var element = elements[j];

      // Add the label
      doc.text(20, yPos, element.labels[0].textContent);

      // Add the value
      doc.text(60, yPos, element.value);

      // Increment the vertical position
      yPos += 10;
    }
  }

  // Save the document as a file
  doc.save("forms.pdf");
}
