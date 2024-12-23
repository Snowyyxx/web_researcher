let currentQuestions = [];
let currentAnswers = [];

document.getElementById('submit-btn').addEventListener('click', async () => {
    const topic = document.getElementById('topic-input').value.trim();
    if (!topic) return;

    try {
        const response = await fetch('/generate-questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        currentQuestions = await response.json();
        displayQuestions(currentQuestions);
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating questions. Please try again.');
    }
});

document.getElementById('fetch-answers-btn').addEventListener('click', async () => {
    if (!currentQuestions.length) return;

    try {
        const response = await fetch('/fetch-answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentQuestions)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const answers = await response.json();
        displayAnswers(answers);
    } catch (error) {
        console.error('Error:', error);
        alert('Error fetching answers. Please try again.');
    }
});

document.getElementById('generate-summary-btn').addEventListener('click', async () => {
    if (!currentAnswers.length) return;

    try {
        const response = await fetch('/generate-summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentAnswers)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const summary = await response.json();
        displaySummary(summary);
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating summary. Please try again.');
    }
});

function displayQuestions(questions) {
    const questionsList = document.getElementById('questions-list');
    questionsList.innerHTML = '';
    
    if (!Array.isArray(questions)) {
        console.error('Expected array of questions, got:', questions);
        return;
    }
    
    questions.forEach(question => {
        const li = document.createElement('li');
        li.className = 'p-4 bg-base-200 rounded-lg';
        li.textContent = question;
        questionsList.appendChild(li);
    });

    document.getElementById('questions-section').classList.remove('hidden');
}

function displayAnswers(answers) {
    currentAnswers = answers;
    const answersList = document.getElementById('answers-list');
    answersList.innerHTML = '';
    
    if (!Array.isArray(answers)) {
        console.error('Expected array of answers, got:', answers);
        return;
    }
    
    answers.forEach((answer, index) => {
        const div = document.createElement('div');
        div.className = 'card bg-base-200 p-4';
        div.innerHTML = `
            <h3 class="font-semibold mb-2">${currentQuestions[index]}</h3>
            <p>${answer}</p>
        `;
        answersList.appendChild(div);
    });

    document.getElementById('answers-section').classList.remove('hidden');
}

function displaySummary(summary) {
    const summaryContent = document.getElementById('summary-content');
    summaryContent.textContent = summary;
    document.getElementById('summary-section').classList.remove('hidden');
} 