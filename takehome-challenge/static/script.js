document.addEventListener('DOMContentLoaded', (event) => {
    const textInput = document.getElementById('text-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const result = document.getElementById('result');
    const history = document.getElementById('history');

    analyzeBtn.addEventListener('click', () => {
        const text = textInput.value;
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text: text}),
        })
        .then(response => response.json())
        .then(data => {
            result.innerHTML = `
                <p>Sentiment: ${data.sentiment}</p>
                <p>Polarity: ${data.polarity.toFixed(2)}</p>
                <p>Subjectivity: ${data.subjectivity.toFixed(2)}</p>
            `;
            updateHistory();
        });
    });

    function updateHistory() {
        fetch('/history')
        .then(response => response.json())
        .then(data => {
            history.innerHTML = '';
            data.forEach(item => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${item.sentiment}</strong> 
                    (Polarity: ${item.polarity.toFixed(2)}, 
                    Subjectivity: ${item.subjectivity.toFixed(2)})
                    <br>
                    <small>"${item.text.substring(0, 100)}${item.text.length > 100 ? '...' : ''}"</small>
                `;
                history.appendChild(li);
            });
        });
    }

    updateHistory();
});
