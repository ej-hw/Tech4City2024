document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadLink = document.getElementById('uploadLink');
    const resultsTable = document.getElementById('resultsTable');
    const enlargedView = document.getElementById('enlargedView');
    const pastDetections = document.getElementById('pastDetections');

    uploadBtn.addEventListener('click', function() {
        fileInput.click();
    });

    uploadLink.addEventListener('click', function(e) {
        e.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            uploadImage(file);
        }
    });

    function uploadImage(file) {
        const formData = new FormData();
        formData.append('image', file);

        // Update table to show uploading status
        updateTable('Uploading...', file.name);

        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            updateTable('Completed', file.name);
            showEnlargedView(data);
            addToPastDetections(data);
        })
        .catch(error => {
            console.error('Error:', error);
            updateTable('Error', file.name);
        });
    }

    function updateTable(status, fileName) {
        const tbody = resultsTable.querySelector('tbody');
        tbody.innerHTML = `
            <tr>
                <td>${fileName}</td>
                <td>${status}</td>
            </tr>
        `;
    }

    function showEnlargedView(data) {
        enlargedView.innerHTML = `
            <img src="data:image/jpeg;base64,${data.image}" alt="Detected Objects">
            <p>Detected Objects: ${data.objects.join(', ')}</p>
        `;
    }

    function addToPastDetections(data) {
        const detectionItem = document.createElement('div');
        detectionItem.className = 'past-detection-item';
        detectionItem.innerHTML = `
            <img src="data:image/jpeg;base64,${data.image}" alt="Past Detection">
            <p>Detected: ${data.objects.join(', ')}</p>
        `;
        pastDetections.prepend(detectionItem);
    }
});