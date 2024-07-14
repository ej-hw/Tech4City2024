// function previewImage(event) {
//     var reader = new FileReader();
//     reader.onload = function(){
//         var output = document.getElementById('imagePreview');
//         output.src = reader.result;
//         output.style.display = 'block';
//     };
//     reader.readAsDataURL(event.target.files[0]);
// }

document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    if (result.image_data) {
        document.getElementById('imagePreview').src = 'data:image/jpeg;base64,' + result.image_data;
        document.getElementById('imagePreview').classList.remove('d-none');
    }
    if (result.prediction) {
        document.getElementById('predictionText').textContent = result.prediction;
        document.getElementById('predictionText').classList.remove('d-none');
    }
});

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.getElementById('imagePreview');
        output.src = reader.result;
        output.classList.remove('d-none');
    };
    reader.readAsDataURL(event.target.files[0]);
}