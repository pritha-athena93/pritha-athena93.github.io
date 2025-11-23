/**
 * Claude-like Chat Interface
 * Handles chat messages and interactions with the AI backend
 */

// Configuration - Cloud Run service URL
const API_ENDPOINT = 'https://career-agent-api-tvpksobx5a-uc.a.run.app';

// Chat state
let isProcessing = false;

/**
 * Send a message to the AI
 */
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isProcessing) {
        return;
    }

    // Clear input
    input.value = '';
    adjustTextareaHeight(input);

    // Add user message to chat
    addMessage(message, 'user');

    // Show loading indicator
    const loadingId = addLoadingMessage();

    // Disable input
    setInputDisabled(true);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const answer = data.answer || data.response || 'No answer received.';
        
        // Remove loading and add AI response
        removeLoadingMessage(loadingId);
        addMessage(answer, 'assistant');
        
    } catch (error) {
        console.error('Error sending message:', error);
        removeLoadingMessage(loadingId);
        addMessage(`Sorry, I encountered an error: ${error.message}. Please try again.`, 'assistant', true);
    } finally {
        setInputDisabled(false);
        input.focus();
    }
}

/**
 * Add a message to the chat
 */
function addMessage(text, type, isError = false) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = type === 'user' ? '👤' : '🤖';
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = avatar;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = isError ? 'message-text error-message' : 'message-text';
    
    // Format text (basic markdown-like formatting)
    textDiv.innerHTML = formatMessage(text);
    
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

/**
 * Format message text (basic markdown support)
 */
function formatMessage(text) {
    // Escape HTML first
    let formatted = escapeHtml(text);
    
    // Convert **bold** to <strong>
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Convert line breaks to <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Convert bullet points
    formatted = formatted.replace(/^[\*\-]\s+(.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    // Wrap in paragraphs
    const paragraphs = formatted.split('<br><br>');
    formatted = paragraphs.map(p => p.trim() ? `<p>${p}</p>` : '').join('');
    
    return formatted;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Add loading indicator
 */
function addLoadingMessage() {
    const messagesContainer = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant-message loading-message';
    loadingDiv.id = 'loading-message';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const dotsDiv = document.createElement('div');
    dotsDiv.className = 'loading-dots';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'loading-dot';
        dotsDiv.appendChild(dot);
    }
    
    contentDiv.appendChild(dotsDiv);
    loadingDiv.appendChild(avatarDiv);
    loadingDiv.appendChild(contentDiv);
    messagesContainer.appendChild(loadingDiv);
    
    scrollToBottom();
    return 'loading-message';
}

/**
 * Remove loading indicator
 */
function removeLoadingMessage(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Adjust textarea height based on content
 */
function adjustTextareaHeight(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

/**
 * Set input disabled state
 */
function setInputDisabled(disabled) {
    isProcessing = disabled;
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendButton');
    
    input.disabled = disabled;
    button.disabled = disabled;
}

/**
 * Initialize chat interface
 */
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendButton');
    
    // Auto-resize textarea
    input.addEventListener('input', function() {
        adjustTextareaHeight(this);
    });
    
    // Send on Enter (Shift+Enter for new line)
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Focus input on load
    input.focus();
    
    // Click handler for send button
    button.addEventListener('click', sendMessage);
});
