// document.getElementById('fileInput').addEventListener('change', function(event) {
//     const file = event.target.files[0];
//     if (!file) {
//         return;
//     }

//     const formData = new FormData();
//     formData.append('file', file);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert(data.error);
//             return;
//         }

//         const imgContainer = document.getElementById('imageContainer');
//         imgContainer.innerHTML = `<img src="data:image/png;base64,${data.processed_image}" alt="Processed Image">`;

//         const predictionContainer = document.getElementById('predictionContainer');
//         predictionContainer.innerHTML = '<h2>Predicted Objects</h2>';
//         predictionContainer.innerHTML += `<pre>${JSON.stringify(data.prediction, null, 2)}</pre>`;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });
document.getElementById('fileInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (!file) {
        return;
    }

    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    xhr.upload.onloadstart = function() {
        document.getElementById('loadingIndicator').style.display = 'block';
    };

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                displayImage(response.image, response.processed_image, response.prediction);
            } else {
                console.error('Upload failed: ' + xhr.status);
            }
            document.getElementById('loadingIndicator').style.display = 'none';
        }
    };

    xhr.send(formData);
});

function displayImage(originalImage, processedImage, predictionData) {
    var imageContainer = document.getElementById('imageContainer');
    var predictionContainer = document.getElementById('predictionContainer');

    imageContainer.innerHTML = '<img src="data:image/png;base64,' + processedImage + '" alt="Processed Image">';
    predictionContainer.innerHTML = '<h2>Predicted Objects</h2>';
    predictionContainer.innerHTML += '<pre>' + JSON.stringify(predictionData, null, 2) + '</pre>';
}