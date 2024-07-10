async function predictSentiment() {
    const review = document.getElementById('review').value;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ review: review }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const result = await response.json();
        if (result.error) {
            document.getElementById('result').innerText = 'Error predicting sentiment.';
        } else {
            document.getElementById('result').innerText = `Predicted Sentiment: ${result.sentiment}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error predicting sentiment.';
    }
}
