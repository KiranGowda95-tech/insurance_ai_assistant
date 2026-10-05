import React from 'react';

export const Chat = () => {
  const suggestions = [
    'What is the status of claim CLM300500?',
    'Which documents are missing?',
    'What is the maternity waiting period?',
    'Is this treatment covered under my policy?',
  ];
  return (
    <>
      <main className='chat-page'>
        {/* Header */}
        <header>
          <div>
            <h1>Insurance AI Assistant</h1>
            <p>Ask questions about claims, policies,coverage and documents.</p>
          </div>
          <div className='system-status'>
            <span className='status-dot'></span>
            System Online
          </div>
        </header>
        {/* Welcome */}
        <section className='welcome-section'>
          <div className='welcome-icon'>✦🤖</div>
          <h2>How can I help you Today?</h2>
          <p>
            I can help you analyze claims, understand policy coverage,check
            missing documents and find insurance information .
          </p>
        </section>
        {/* Search */}
        <section className='chat-input-section'>
          <div className='chat-input-wrapper'>
            <input
              type='text'
              placeholder='Ask about a claim,policy,coverage or documents...'
            />
            <button>➤</button>
          </div>
        </section>
        {/* Suggestions */}
        <section className='suggestions-section'>
          <p className='suggestion-title'>Suggestion Questions</p>
          <div className='suggestion-grid'>
            {suggestions.map((question, index) => (
              <button key={index} className='suggestion-card'>
                <span>✦</span>
                <p>{question}</p>
                <span className='arrow'>→</span>
              </button>
            ))}
          </div>
        </section>
      </main>
    </>
  );
};
