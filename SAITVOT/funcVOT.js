// script.js

document.getElementById("file-upload").addEventListener("change", function(event) {
    const files = event.target.files;
    const previewContainer = document.getElementById("preview-container");

    // Clear previous previews
    previewContainer.innerHTML = "<p>Preview:</p>";

    Array.from(files).forEach(file => {
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            const imgElement = document.createElement("img");
            imgElement.classList.add("preview-image");

            reader.onload = function(e) {
                imgElement.src = e.target.result;
                previewContainer.appendChild(imgElement);
            };

            reader.readAsDataURL(file);
        }
    });
});
