/**
 * SOP (Standard Operating Procedure) Script for AI Agent
 * 
 * This script handles the interaction between the frontend and the AI agent backend.
 * It sends questions to the Cloud Run API and displays responses.
 */

// Configuration - Cloud Run service URL
const API_ENDPOINT = 'https://career-agent-api-tvpksobx5a-uc.a.run.app';

/**
 * Main function to handle question submission
 */
async function askQuestion() {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    if (!question) {
        alert('Please enter a question.');
        return;
    }

    // Show loading, hide previous answers/errors
    showLoading();
    hideAnswer();
    hideError();

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayAnswer(data.answer || data.response || 'No answer received.');
        
    } catch (error) {
        console.error('Error asking question:', error);
        showError(`Failed to get answer: ${error.message}. Please check that the API endpoint is configured correctly.`);
    } finally {
        hideLoading();
    }
}

/**
 * Display the answer from the AI agent
 */
function displayAnswer(answer) {
    const answerSection = document.getElementById('answerSection');
    const answerContent = document.getElementById('answerContent');
    
    answerContent.textContent = answer;
    answerSection.style.display = 'block';
    
    // Scroll to answer
    answerSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show loading indicator
 */
function showLoading() {
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('askButton').disabled = true;
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    document.getElementById('loadingIndicator').style.display = 'none';
    document.getElementById('askButton').disabled = false;
}

/**
 * Show error message
 */
function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

/**
 * Hide answer section
 */
function hideAnswer() {
    document.getElementById('answerSection').style.display = 'none';
}

/**
 * Allow Enter key to submit (Shift+Enter for new line)
 */
document.addEventListener('DOMContentLoaded', function() {
    const questionInput = document.getElementById('questionInput');
    
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
        }
    });
});

