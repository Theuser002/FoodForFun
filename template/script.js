//selecting all required elements
let dropArea = document.querySelector(".drag-area"),
  dragText = document.querySelector("header"),
  button = document.querySelector(".browse"),
  input = document.querySelector("input"),
  upload = dropArea.querySelector(".upload-img"),
  h2 = document.querySelector("h2")

var chooseAnotherImgButton = document.createElement("button")
chooseAnotherImgButton.classList.add("another-file")
chooseAnotherImgButton.innerHTML = "Choose another image";

var submitButton = document.createElement("input")
submitButton.classList.add("submit-btn")
submitButton.value = "Submit";
submitButton.type = "submit"
submitButton.onclick = () => {
  showResult();
}

function showResult() {
  location.replace("result.html")
}

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

let file; //this is a global variable and we'll use it inside multiple functions

button.onclick = () => {
  input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function () {
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  // dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function

});

function showFile() {
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) { //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; //passing user file source in fileURL variable
      let imgTag = `<img class="upload-img" src="${fileURL}" alt="">`; //creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container

      chooseAnotherImgButton.onclick = () => {
        input.click(); //if user click on the button then the input also clicked
      }
      insertAfter(h2, chooseAnotherImgButton);
      insertAfter(dropArea, submitButton);
    }
    fileReader.readAsDataURL(file);
  } else {
    dragText.innerHTML = "This is not an Image File! <button class='refresh' onClick='window.location.reload();'>Refresh Page</button>";
    dropArea.classList.remove("active");
    // dragText.innerHTML = "Drag & Drop to Upload File OR <button class='browse'>Browse File</button>";
  }
}
