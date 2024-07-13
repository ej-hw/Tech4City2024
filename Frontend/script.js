let currentAnalysisId = null;

document.getElementById('sentiment-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const textInput = document.getElementById('text-input').value;

    const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
    });

    const result = await response.json();
    currentAnalysisId = result.id;
    displayResult(result);
    fetchResults();
});

async function fetchResults() {
    const response = await fetch('http://localhost:8000/results');
    const results = await response.json();

    let historyHtml = '';
    results.reverse().forEach(result => {
        let sentimentText = getSentimentText(result[2]);
        let feedbackText = result[4] !== null ? getSentimentText(result[4]) : '-';
        let correct = result[3] === 'correct' ? 'Yes' : (result[3] ? 'No' : 'N/A');
        let feedbackForm = '';
        if (!result[3]) {
            feedbackForm = `<form onsubmit="submitFeedback(event, ${result[0]})">
                                <h5>Is the sentiment correct?</h5>
                                <input type="radio" id="feedback-correct-${result[0]}" name="feedback-${result[0]}" value="correct" onclick="toggleCorrectSentiment(${result[0]}, false)">
                                <label for="feedback-correct-${result[0]}">Yes</label><br>
                                <input type="radio" id="feedback-incorrect-${result[0]}" name="feedback-${result[0]}" value="incorrect" onclick="toggleCorrectSentiment(${result[0]}, true)">
                                <label for="feedback-incorrect-${result[0]}">No</label><br>
                                <div id="correct-sentiment-${result[0]}" style="display: none;">
                                    <h5>Please provide the correct sentiment:</h5>
                                    <input type="radio" id="feedback-pos-${result[0]}" name="correct-feedback-${result[0]}" value="1">
                                    <label for="feedback-pos-${result[0]}">Positive</label><br>
                                    <input type="radio" id="feedback-neu-${result[0]}" name="correct-feedback-${result[0]}" value="0">
                                    <label for="feedback-neu-${result[0]}">Neutral</label><br>
                                    <input type="radio" id="feedback-neg-${result[0]}" name="correct-feedback-${result[0]}" value="-1">
                                    <label for="feedback-neg-${result[0]}">Negative</label><br>
                                </div>
                                <button type="submit">Submit Feedback</button>
                            </form>`;
        }
        historyHtml += `<tr>
                            <td>${result[1]}</td>
                            <td>${sentimentText}</td>
                            <td>${feedbackText}</td>
                            <td>${correct}</td>
                            <td>${feedbackForm}</td>
                        </tr>`;
    });

    document.getElementById('history-body').innerHTML = historyHtml;
}

function displayResult(result) {
    let sentimentText = getSentimentText(result.sentiment);
    document.getElementById('sentiment-label').innerText = `Sentiment: ${sentimentText}`;
}

function getSentimentText(sentimentValue) {
    if (sentimentValue === 1) {
        return 'Positive';
    } else if (sentimentValue === 0) {
        return 'Neutral';
    } else if (sentimentValue === -1) {
        return 'Negative';
    } else if (sentimentValue === 'correct') {
        return '-';
    }
    return 'Unknown';
}

function toggleCorrectSentiment(id, show) {
    const correctSentimentDiv = document.getElementById(`correct-sentiment-${id}`);
    correctSentimentDiv.style.display = show ? 'block' : 'none';
}

document.getElementById('feedback-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const feedbackValue = document.querySelector('input[name="feedback"]:checked').value;

    let feedbackData = { id: currentAnalysisId, feedback: feedbackValue };
    if (feedbackValue === 'incorrect') {
        const correctFeedbackValue = document.querySelector('input[name="correct-feedback"]:checked').value;
        feedbackData.correct_feedback = correctFeedbackValue;
    }

    const response = await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
    });

    const result = await response.json();
    if (result.status === 'success') {
        alert('Feedback submitted successfully');
        fetchResults();
        document.getElementById('feedback').style.display = 'none';
    }
});

async function submitFeedback(event, id) {
    event.preventDefault();
    const feedbackValue = document.querySelector(`input[name="feedback-${id}"]:checked`).value;

    let feedbackData = { id: id, feedback: feedbackValue };
    if (feedbackValue === 'incorrect') {
        const correctFeedbackValue = document.querySelector(`input[name="correct-feedback-${id}"]:checked`).value;
        feedbackData.correct_feedback = correctFeedbackValue;
    }

    const response = await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
    });

    const result = await response.json();
    if (result.status === 'success') {
        alert('Feedback submitted successfully');
        fetchResults();
    }
}

document.addEventListener('DOMContentLoaded', fetchResults);
