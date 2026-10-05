import React from 'react';

export const ChatInput = ({ input, setInput, handleSend }) => {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };
  return (
    <section className='chat-input-section'>
      <div className='chat-input-wrapper'>
        <input
          type='text'
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder='Ask about a claim,policy,coverage or document...'
        />
        <button onClick={handleSend} disabled={!input.trim()}>
          {' '}
          ➤
        </button>
      </div>
    </section>
  );
};
