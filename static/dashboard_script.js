/*document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.querySelector(".drop_box");
    const button = dropArea.querySelector("button");
    const input = dropArea.querySelector("input");
    let file;
    let filename;
  
    button.addEventListener("click", () => {
      input.click();
    });
  
    input.addEventListener("change", function (e) {
      file = e.target.files[0]; // Store the selected file
      filename = file.name; // Get the file name
  
      if (file.type.includes('text')) {
        const reader = new FileReader();
        reader.onload = function (event) {
          const text = event.target.result;
          // Display the text content in dropArea
          dropArea.innerHTML = `<p>${filename}</p><pre>${text}</pre>`;
        };
        reader.readAsText(file);
      } else {
        // Display the file name if it's not a text file
        dropArea.innerHTML = `<p>${filename}</p>`;
      }
    });
  });*/
  