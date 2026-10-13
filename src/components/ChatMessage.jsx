import ReactMarkdown from 'react-markdown';

export const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';

  // The model sometimes puts headings on the same line.
  // Add line breaks so Markdown can recognize those headings.
  const content =
    typeof message.content === 'string'
      ? message.content.replace(/\s+(#{1,6}\s)/g, '\n\n$1')
      : '';

  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className='message-avatar'>{isUser ? 'A' : '✦'}</div>

      <div className='message-content'>
        <span className='message-role'>{isUser ? 'You' : 'Insurance AI'}</span>

        <div className='message-text'>
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{content}</ReactMarkdown>
          )}
        </div>
      </div>
    </div>
  );
};
