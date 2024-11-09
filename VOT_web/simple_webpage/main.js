async function uploadImage() {
    const formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);
    formData.append('description', document.getElementById('description').value);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        document.getElementById('message').textContent = result.message;

        // Reload gallery
        loadGallery();
    } catch (error) {
        console.error('Error uploading image:', error);
        document.getElementById('message').textContent = 'Failed to upload image';
    }
}

async function loadGallery() {
    try {
        const response = await fetch('http://localhost:5000/gallery');
        const images = await response.json();

        const gallery = document.getElementById('gallery');
        gallery.innerHTML = '';  // Clear existing content

        images.forEach(image => {
            const imgElem = document.createElement('img');
            imgElem.src = `http://localhost:5000/uploads/${image.filename}`;
            imgElem.alt = image.description;

            const descElem = document.createElement('p');
            descElem.textContent = image.description;

            const container = document.createElement('div');
            container.appendChild(imgElem);
            container.appendChild(descElem);

            gallery.appendChild(container);
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
    }
}

// Load gallery on page load
document.addEventListener('DOMContentLoaded', loadGallery);
