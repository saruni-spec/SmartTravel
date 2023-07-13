function downloadAsDoc() {
    var doc = new jsPDF();
  
    // Get the form elements
    var form = document.getElementById("myForm");
    var elements = form.elements;
  
    // Set the initial vertical position
    var yPos = 20;
  
    // Loop through the form elements and add them to the document
    for (var i = 0; i < elements.length; i++) {
      var element = elements[i];
  
      // Add the label
      doc.text(20, yPos, element.labels[0].textContent);
  
      // Add the value
      doc.text(60, yPos, element.value);
  
      // Increment the vertical position
      yPos += 10;
    }
  
    // Save the document as a file
    doc.save("form.doc");
  }