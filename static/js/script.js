//selecting all required elements
var dropArea = document.querySelector(".drag-area"),
    dragText = document.querySelector("header"),
    button = document.querySelector(".browse"),
    input = document.querySelector("#input"),
    upload = dropArea.querySelector(".upload-img"),
    h2 = document.querySelector("h2"),
    labelBrowse = document.querySelector("#labelBrowse"),
    labelUrl = document.querySelector("#labelUrl"),
    imageURL = document.querySelector("#imageURL"),
    imageURLDiv = document.querySelector(".imageURLDiv"),
    imageURLInput = document.querySelector("#imageURLInput"),
    linkArea = document.querySelector(".link-area"),
    row = document.querySelector(".row"),
    form = document.getElementById("imageForm")

var chooseAnotherImgButton = document.createElement("button")
chooseAnotherImgButton.classList.add("another-file")
chooseAnotherImgButton.innerHTML = "Choose another image";

const submitButton = document.createElement("input")
submitButton.classList.add("submit-btn")
submitButton.value = "Submit";
submitButton.type = "submit"
submitButton.onclick = () => {
    submitImage();
}

var submitButton2 = document.createElement("input")
submitButton2.classList.add("submit-btn")
submitButton2.value = "Submit";
submitButton2.type = "submit"
submitButton2.onclick = () => {
    submitImage();
}
var array = ["Xception", "MobileNetV2"];

const submitDiv = document.createElement("div")
submitDiv.classList.add("d-flex")

const selectModel = document.createElement("select")
selectModel.classList.add("form-control")
selectModel.name = "model"
selectModel.id = "model"

//Create and append the options
for (var i = 0; i < array.length; i++) {
    var option = document.createElement("option");
    option.value = array[i];
    option.text = array[i];
    selectModel.appendChild(option);
}

submitDiv.appendChild(selectModel)
submitDiv.appendChild(submitButton)

labelBrowse.onclick = () => {
    dropArea.style.display = "block";
    imageURLDiv.style.display = "none";
    dropArea.classList.remove("active");
    submitDiv.remove();
    chooseAnotherImgButton.remove();
    dropArea.innerHTML = "<header>Drag & Drop to Upload File OR <a class='browse'>Browse File</a></header>"
    document.querySelector(".browse").addEventListener("click", (event) => {
        event.preventDefault();
        input.click(); //if user click on the button then the input also clicked
    });
}

labelUrl.onclick = () => {
    dropArea.style.display = "none";
    imageURLDiv.style.display = "block";
    submitDiv.remove();
    chooseAnotherImgButton.remove();
    linkArea.innerHTML = "";
    imageURLInput.value = ""
}


imageURLInput.addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        showImageFromURL();
    }
});


function submitImage() {
    form.action = "/predict";
    form.submit();
}

function showResult() {
    location.replace("result.html")
}

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

let file; //this is a global variable and we'll use it inside multiple functions

button.addEventListener("click", (event) => {
    event.preventDefault();
    input.click(); //if user click on the button then the input also clicked
});

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
            let imgTag = `<img class="upload-img" id="drop-img" src="${fileURL}" alt="">`; //creating an img tag and passing user selected file source inside src attribute
            dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
            imageURL.value = fileURL;

            chooseAnotherImgButton.onclick = () => {
                input.click(); //if user click on the button then the input also clicked
            }
            insertAfter(row, chooseAnotherImgButton);
            insertAfter(dropArea, submitDiv);
            document.getElementById("denoiseCheckbox").disabled = false

        }
        fileReader.readAsDataURL(file);
    } else {
        dragText.innerHTML = "This is not an Image File! <button class='refresh' onClick='window.location.reload();'>Refresh Page</button>";
        dropArea.classList.remove("active");
        // dragText.innerHTML = "Drag & Drop to Upload File OR <button class='browse'>Browse File</button>";
    }
}

function showImageFromURL() {
    insertAfter(dropArea, submitDiv);
    document.getElementById("denoiseCheckbox").disabled = false
    let imgTag = `<img class="upload-img" id="link-img" src="${imageURLInput.value}" alt="">`; //creating an img tag and passing user selected file source inside src attribute
    linkArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
    imageURL.value = imageURLInput.value;
}
