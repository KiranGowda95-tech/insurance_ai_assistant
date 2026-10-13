import { useEffect, useRef, useState } from 'react';

import { ChatHeader } from '../components/ChatHeader';
import { ChatMessage } from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';
import { SuggestionCard } from '../components/SuggestionCard';

import { sendMessage } from '../services/api';

export const Chat = () => {
  const [input, setInput] = useState('');

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  // Reference to the bottom of the chat messages
  const messagesEndRef = useRef(null);

  const suggestions = [
    'What is the status of claim CLM300001?',
    'Which documents are missing for claim CLM300001?',
    'What is the maternity waiting period?',
    'What is covered under my insurance policy?',
  ];

  // ==========================================
  // AUTO SCROLL TO LATEST MESSAGE
  // ==========================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    });
  }, [messages, loading]);

  // ==========================================
  // WHEN USER CLICKS A SUGGESTION
  // ==========================================

  const handleSuggestionClick = (question) => {
    setInput(question);
  };

  // ==========================================
  // SEND MESSAGE
  // ==========================================

  const handleSend = async () => {
    // Prevent empty messages
    if (!input.trim()) {
      return;
    }

    if (loading) {
      return;
    }

    const question = input.trim();

    // ==========================================
    // CREATE USER MESSAGE
    // ==========================================

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: question,
    };

    // Add user message
    setMessages((previousMessages) => [...previousMessages, userMessage]);

    // Clear input
    setInput('');

    // Show loading state
    setLoading(true);

    try {
      // ==========================================
      // CALL API
      // ==========================================

      const response = await sendMessage(question, messages);

      // ==========================================
      // CREATE AI MESSAGE
      // ==========================================

      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.answer,
      };

      // Add AI response
      setMessages((previousMessages) => [...previousMessages, aiMessage]);
    } catch (error) {
      console.error('Error while sending message:', error);

      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Sorry, I couldn't process your question. ${
          error.message || 'Please check that the backend is running.'
        }`,
      };

      setMessages((previousMessages) => [...previousMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className='chat-page'>
      {/* ==========================================
          HEADER
      ========================================== */}

      <ChatHeader />

      {/* ==========================================
          CHAT CONTAINER
      ========================================== */}

      <section className='chat-container'>
        {/* ==========================================
            SCROLLABLE CHAT AREA
        ========================================== */}

        <div className='chat-messages-area'>
          {/* ========================================
              EMPTY CHAT STATE
          ======================================== */}

          {messages.length === 0 ? (
            <div className='empty-chat'>
              {/* Welcome */}

              <div className='welcome-section'>
                <div className='welcome-icon'>✦</div>

                <h2>How can I help you today?</h2>

                <p>
                  I can help you analyze claims, understand policy coverage,
                  check missing documents and find insurance information.
                </p>
              </div>

              {/* Suggested Questions */}

              <section className='suggestions-section'>
                <p className='suggestion-title'>Suggested Questions</p>

                <div className='suggestion-grid'>
                  {suggestions.map((question, index) => (
                    <SuggestionCard
                      key={index}
                      question={question}
                      onClick={handleSuggestionClick}
                    />
                  ))}
                </div>
              </section>
            </div>
          ) : (
            /* ========================================
               CHAT MESSAGES
            ======================================== */

            <div className='messages-container'>
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}

              {/* ======================================
                  LOADING / AI THINKING
              ====================================== */}

              {loading && (
                <div className='message ai-message'>
                  <div className='message-avatar'>✦</div>

                  <div className='message-content'>
                    <span className='message-role'>Insurance AI</span>

                    <p className='typing'>Analyzing your question...</p>
                  </div>
                </div>
              )}

              {/* ======================================
                  AUTO SCROLL TARGET
              ====================================== */}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* ==========================================
            FIXED BOTTOM INPUT AREA
        ========================================== */}

        <div className='chat-input-area'>
          <ChatInput
            input={input}
            setInput={setInput}
            handleSend={handleSend}
            loading={loading}
          />
        </div>
      </section>
    </main>
  );
};
