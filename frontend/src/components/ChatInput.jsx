function ChatInput({ input, setInput, handleSend, loading }) {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !loading) {
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
          disabled={loading}
          placeholder={
            loading
              ? 'Insurance AI is analyzing...'
              : 'Ask about a claim, policy, coverage or document...'
          }
        />

        <button onClick={handleSend} disabled={!input.trim() || loading}>
          {loading ? '...' : '➤'}
        </button>
      </div>
    </section>
  );
}

export default ChatInput;
