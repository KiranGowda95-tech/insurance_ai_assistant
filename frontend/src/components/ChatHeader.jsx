import React from 'react';

export const ChatHeader = () => {
  return (
    <header className='top-header'>
      <div>
        <h1>Insurance AI Assistant</h1>
        <p>Ask questions about claims,policies,coverage and documents</p>
      </div>
      <div className='system-status'>
        <span className='status-d'></span>
        System Online
      </div>
    </header>
  );
};
