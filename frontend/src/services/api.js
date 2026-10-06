const API_BASE_URL = 'http://localhost:8000';

export async function sendMessage(question) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        answer:
          'This is a temporary response from the insurance AI Assistance123456',
        route: 'SQL',
        sources: [
          {
            type: 'database',
            name: 'claims',
          },
        ],
      });
    }, 1000);
  });
}
