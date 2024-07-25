function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);
        fetch('/images/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
}