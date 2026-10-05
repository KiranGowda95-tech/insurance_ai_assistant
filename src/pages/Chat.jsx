import { useState } from 'react';
import { ChatHeader } from '../components/ChatHeader';
import { ChatMessage } from '../components/ChatMessage';
import { ChatInput } from '../components/ChatInput';
import { SuggestionCard } from '../components/SuggestionCard';

import { sendMessage } from '../services/api';

export const Chat = () => {
  const [input, setInput] = useState('');

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const suggestions = [
    'What is the status of claim CLM300500?',
    'Which documents are missing?',
    'What is the maternity waiting period?',
    'Is this treatment covered under my policy?',
  ];

  //when user clicks on a suggestion
  const handleSuggestionClick = (question) => {
    setInput(question);
  };

  //Send message
  const handleSend = async () => {
    //not to send the empty messages
    if (!input.trim()) {
      return;
    }

    const question = input.trim();

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: question,
    };

    //Add user message to chat
    setMessages((previousMessages) => [...previousMessages, userMessage]);

    //to clear the input field
    setInput('');

    //to show loading
    setLoading(true);

    try {
      const response = await sendMessage(question);

      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.answer,
      };

      setMessages((previousMessages) => [...previousMessages, aiMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, something went wrong while processing your request...',
      };

      setMessages((previousMessages) => [...previousMessages, errorMessage]);
    } finally {
      setLoading(false);
    }

    //temporary fake AI response till the backend is ready
    // setTimeout(() => {
    //   const aiMessage = {
    //     id: Date.now() + 1,
    //     role: 'assistant',
    //     content:
    //       "I'm analyzing your question.This is a temporary response until the backend is ready.",
    //   };
    //   setMessages((previousMessages) => [...previousMessages, aiMessage]);
    //   setLoading(false);
    // }, 1000);
  };

  // const handleKeyDown = (event) => {
  //   if (event.key === 'Enter') {
  //     handleSend();
  //   }
  // };

  return (
    <main className='chat-page'>
      {/* Header */}
      {/* <header className='top-header'>
        <div>
          <h1>Insurance AI Assistant</h1>
          <p>Ask questions about claims, policies,coverage and documents.</p>
        </div>
        <div className='system-status'>
          <span className='status-dot'></span>
          System Online
        </div>
      </header> */}
      <ChatHeader />

      {/* chat content */}

      <section className='chat-container'>
        {messages.length === 0 ? (
          <div className='welcome-section'>
            <div className='welcome-icon'>✦</div>
            <h2>How can I help you today?</h2>
            <p>
              I can help you analyze claims, understand policy coverage,check
              missing documents and find insurance information .
            </p>
          </div>
        ) : (
          <div className='messages-container'>
            {messages.map((message) => (
              // <div
              //   key={message.id}
              //   className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
              // >
              //   <div className='message-avatar'>
              //     {message.role === 'user' ? 'A' : '✦'}
              //   </div>
              //   <div className='message-content'>
              //     <span className='message-role'>
              //       {message.role === 'user' ? 'You' : 'Insurance AI'}
              //     </span>
              //     <p>{message.content}</p>
              //   </div>
              // </div>
              <ChatMessage key={message.id} message={message} />
            ))}
            {/* Loading */}
            {loading && (
              <div className='message ai-message'>
                <div className='message-avatar'>✦</div>
                <div className='message-content'>
                  <span className='message-role'>Insurance AI</span>
                  <p className='typing'>Analyzing your question...</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Input Search*/}
        {/* <section className='chat-input-section'>
          <div className='chat-input-wrapper'>
            <input
              type='text'
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder='Ask about a claim,policy,coverage or documents...'
            />
            <button onClick={handleSend} disabled={!input.trim()}>
              ➤
            </button>
          </div>
        </section> */}
        <ChatInput input={input} setInput={setInput} handleSend={handleSend} />

        {/* Suggestions */}
        {messages.length === 0 && (
          <section className='suggestions-section'>
            <p className='suggestion-title'>Suggestion Questions</p>
            <div className='suggestion-grid'>
              {suggestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(question)}
                  className='suggestion-card'
                >
                  <span>✦</span>
                  <p>{question}</p>
                  <span className='arrow'>→</span>
                </button>
              ))}
            </div>
          </section>
        )}
      </section>
    </main>
  );
};
