import React, { useState } from 'react'
import './Interface.css'

/**
 * SignInterface - Sign language interface for deaf users
 * 
 * Features:
 * - Sign language avatar
 * - Text chat
 * - Visual alerts
 * - Large text support
 */
const SignInterface = () => {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])

  const handleSendMessage = () => {
    if (message.trim()) {
      setMessages([...messages, { text: message, sender: 'user' }])
      setMessage('')
      
      // Simulate response
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          text: 'Thank you for your message! I understand.', 
          sender: 'system' 
        }])
      }, 1000)
    }
  }

  return (
    <div className="interface-container sign-interface">
      <h2>Sign Language Interface</h2>
      
      <div className="interface-content">
        <div className="sign-avatar-section">
          <div className="sign-avatar">
            <div className="avatar-placeholder">
              <span className="avatar-icon">👋</span>
              <p>Sign Language Avatar</p>
            </div>
          </div>
        </div>

        <div className="chat-section">
          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="empty-chat">
                <p>Start a conversation by typing a message below.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div 
                  key={index} 
                  className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'system-message'}`}
                >
                  <p>{msg.text}</p>
                </div>
              ))
            )}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message here..."
              aria-label="Message input"
              className="large-input"
            />
            <button
              className="btn btn-primary"
              onClick={handleSendMessage}
              aria-label="Send message"
            >
              Send
            </button>
          </div>
        </div>

        <div className="quick-replies">
          <h3>Quick Replies:</h3>
          <div className="reply-buttons">
            <button
              className="btn btn-secondary"
              onClick={() => setMessage('Yes')}
            >
              Yes
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => setMessage('No')}
            >
              No
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => setMessage('Thank you')}
            >
              Thank You
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => setMessage('I need help')}
            >
              I Need Help
            </button>
          </div>
        </div>

        <div className="interface-info">
          <p>This interface is optimized for sign language and visual communication.</p>
        </div>
      </div>
    </div>
  )
}

export default SignInterface

