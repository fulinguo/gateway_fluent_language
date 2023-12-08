document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#questionSubmitForm');
    const chatArea = document.getElementById('chatArea');
    const optionsSection = document.getElementById('options');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const questionInput = form.querySelector('input[name="question"]');
        const question = questionInput.value
        chatArea.innerHTML += `<div class="message user-message"><b>You:</b> ${question}</div>`;
        questionInput.value = '';

        fetch('/get-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `question=${encodeURIComponent(question)}`
        })
        .then(response => response.json())
        .then(data => {
            chatArea.innerHTML += `<p><b>Answer:</b> ${data.answer}</p>`;
            optionsSection.style.display = 'block'; 
        })
        .catch(error => {
            console.error('Error:', error);
        });
        //answerSection.style.display = 'block';
        //optionsSection.style.display = 'flex';
    });

    document.getElementById('moreExamplesBtn').addEventListener('click', function() {
        fetch('/get-examples', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            // No need to send a body as the prompt is not explicitly provided
        })
        .then(response => response.json())
        .then(data => {
            chatArea.innerHTML += `<div class="message bot-message"><b>Bot:</b> ${data.answer}</div>`;
        })
        .catch(error => console.error('Error:', error));
    });
    
    document.getElementById('relatedPhrasesBtn').addEventListener('click', function() {
        fetch('/get-related', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
        .then(response => response.json())
        .then(data => {
            chatArea.innerHTML += `<div class="message bot-message"><b>Bot:</b> ${data.answer}</div>`;
        })
        .catch(error => console.error('Error:', error));
    });
    

    document.getElementById('loginBtn').addEventListener('click', function() {
        window.location.href = '/login';  // Redirect to the login page
    });

    // Event listener for signup button
    document.getElementById('signupBtn').addEventListener('click', function() {
        window.location.href = '/sign_up';  // Redirect to the signup page
    });
});
