import React from 'react';

export const SuggestionCard = ({ question, onClick }) => {
  return (
    <button className='suggestion-card' onClick={() => onClick(question)}>
      <span>✦</span>
      <p>{question}</p>
      <span className='arrow'>→</span>
    </button>
  );
};
