import React from 'react';

export const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';
  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className='message-avatar'>{isUser ? 'A' : '✦'}</div>
      <div className='message-content'>
        <span className='message-role'>{isUser ? 'You' : 'Insurance AI'}</span>
        <p>{message.content}</p>
      </div>
    </div>
  );
};
