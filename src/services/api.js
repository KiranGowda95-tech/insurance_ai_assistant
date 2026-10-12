const API_BASE_URL = 'http://127.0.0.1:8000';

export async function sendMessage(question) {
  console.log('Sending question to API:', question);
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
    }),
  });

  console.log('Response status:', response.status);

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  const data = await response.json();

  return data;

  // return new Promise((resolve) => {
  //   setTimeout(() => {
  //     resolve({
  //       answer:
  //         'This is a temporary response from the insurance AI Assistance123456',
  //       route: 'SQL',
  //       sources: [
  //         {
  //           type: 'database',
  //           name: 'claims',
  //         },
  //       ],
  //     });
  //   }, 1000);
  // });
}
