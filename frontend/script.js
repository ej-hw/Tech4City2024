const video = document.getElementById('video');
const postureResult = document.getElementById('postureResult');
const makePhotoIdButton = document.getElementById('makePhotoIdButton');
const nameForm = document.getElementById('nameForm');
const nameInput = document.getElementById('nameInput');
const photoIdImage = document.getElementById('photoIdImage');
const idName = document.getElementById('idName');

nameForm.addEventListener('submit', function (e) {
    e.preventDefault();
    showAnalysisPage();
});

navigator.mediaDevices.getUserMedia({
    video: true
}).then(stream => {
    video.srcObject = stream;
});

video.addEventListener('play', () => {
    setInterval(async () => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');
        const blob = await fetch(imageData).then(res => res.blob());
        const formData = new FormData();
        formData.append('image', blob, 'image.jpg');

        const response = await fetch('http://localhost:8000/detect', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        displayResult(result.posture);
    }, 1000);
});

function displayResult(posture) {
    if (posture === 'Centralised') {
        postureResult.style.color = 'green';
        makePhotoIdButton.style.display = 'block';
    } else {
        postureResult.style.color = 'red';
        makePhotoIdButton.style.display = 'none';
    }

    postureResult.innerText = posture;
}

function showHomepage() {
    document.getElementById('homepage').style.display = 'block';
    document.getElementById('analysispage').style.display = 'none';
    document.getElementById('idpage').style.display = 'none';
    document.getElementById('submissionsPage').style.display = 'none';
}

function showAnalysisPage() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('analysispage').style.display = 'block';
    document.getElementById('idpage').style.display = 'none';
    document.getElementById('submissionsPage').style.display = 'none';
}

async function makePhotoId() {
    const name = nameInput.value;
    idName.innerText = `Name: ${name}`;

    const formData = new FormData();
    formData.append('name', name);

    const response = await fetch('http://localhost:8000/make_id', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        photoIdImage.src = url;
        showIdPage();
    } else {
        alert('Failed to create photo ID');
    }
}

function showIdPage() {
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('analysispage').style.display = 'none';
    document.getElementById('idpage').style.display = 'block';
    document.getElementById('submissionsPage').style.display = 'none';
}

async function fetchDatabase() {
    const response = await fetch('http://localhost:8000/submissions');
    const submissions = await response.json();
    const submissionsTable = document.getElementById('submissionsTable').getElementsByTagName('tbody')[0];
    submissionsTable.innerHTML = '';

    submissions.forEach(submission => {
        const row = submissionsTable.insertRow();
        const nameCell = row.insertCell(0);
        const timestampCell = row.insertCell(1);
        nameCell.textContent = submission[0];
        timestampCell.textContent = submission[1];
    });
}

function showDatabase() {
    fetchDatabase();
    document.getElementById('homepage').style.display = 'none';
    document.getElementById('analysispage').style.display = 'none';
    document.getElementById('idpage').style.display = 'none';
    document.getElementById('submissionsPage').style.display = 'block';
}

// Initialize homepage
showHomepage();
