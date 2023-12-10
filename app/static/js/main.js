document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#questionSubmitForm');
    const chatArea = document.getElementById('chatArea');
    const optionsSection = document.getElementById('options');

    function appendMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<b>${sender === 'user' ? 'You' : 'AI'}:</b> ${message}`;
        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;  // Scroll to the bottom
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const questionInput = form.querySelector('input[name="question"]');
        const question = questionInput.value
        appendMessage(question, 'user');
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
            appendMessage(data.answer, 'AI');
            optionsSection.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('moreExamplesBtn').addEventListener('click', function() {
        fetch('/get-examples', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.answer, 'AI');
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
            appendMessage(data.answer, 'AI');
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

    // Event listener for settings button
    document.getElementById('settingsBtn').addEventListener('click', function() {
        window.location.href = '/dashboard';  // Redirect to the settings page
    });
});



