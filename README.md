# Enterprise Insurance Claims & Policy Intelligence Assistant

A Gen-AI-powered insurance assistant that answers policy questions, retrieves claim details, checks missing documents, and looks up hospital information through a conversational interface.

## 1. Project Overview

Insurance information is often spread across structured databases and lengthy policy documents. Finding the right claim details or policy conditions manually can take time.

This project combines a React chat interface, a FastAPI backend, a LangGraph agent, structured database tools, and Retrieval-Augmented Generation (RAG) to provide relevant, source-grounded responses.

**Project domain:** Insurance  
**Project type:** Individual Gen-AI practice project

## 2. Key Features

- **Policy question answering:** Retrieves relevant policy passages using hybrid search and reranking.
- **Claim lookup:** Retrieves claim status, amounts, and available claim details.
- **Missing-document detection:** Identifies documents marked as missing for a specific claim.
- **Hospital lookup:** Retrieves hospital information linked to a claim when available.
- **LLM tool calling:** Uses a LangGraph agent to select the appropriate tools for supported questions.
- **Scope validation:** Handles greetings and redirects or declines unrelated requests.
- **Interactive chat:** Provides message history, suggested questions, loading feedback, and error messages.
- **API error handling:** Returns safe error responses when unexpected processing failures occur.

## 3. Technology Stack

| Component                | Technologies                                  |
| ------------------------ | --------------------------------------------- |
| Frontend                 | React, Vite, JavaScript                       |
| Backend API              | Python, FastAPI, Uvicorn                      |
| Agent orchestration      | LangGraph, LangChain                          |
| Language model           | OpenAI API                                    |
| Structured data          | SQLite, SQLAlchemy                            |
| Vector database          | ChromaDB                                      |
| Embeddings and reranking | sentence-transformers                         |
| Hybrid retrieval         | Semantic search, BM25, Reciprocal Rank Fusion |
| Validation               | Pydantic                                      |

## 4. System Architecture

1. The user submits a question through the React chat interface.
2. The frontend sends a POST request to the FastAPI `/api/chat` endpoint.
3. The LangGraph agent validates the request and determines whether it is within scope.
4. The model selects an appropriate tool when necessary.
5. The tools retrieve claim, document, or hospital information from structured data, or search policy documents using the RAG pipeline.
6. The agent generates a response based on the retrieved information.
7. FastAPI returns the result to React, where the answer appears in the chat.

**Architecture flow:**

React + Vite → FastAPI → LangGraph Agent → Tools → SQLite / Policy RAG → Response

## 5. Project Structure

```text
insurance_ai_assistant/
├── backend/
│   ├── agent/
│   ├── data/
│   ├── database/
│   ├── policy_documents/
│   ├── rag/
│   ├── routes/
│   ├── services/
│   ├── main.py
│   ├── requirements.txt
│   └── load_data.py
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── App.jsx
│   └── main.jsx
├── .env.example
├── .gitignore
├── package.json
├── package-lock.json
└── README.md
```

The structure above summarizes the main application components. Supporting scripts, configuration files, and data files may also be present.

## 6. Prerequisites

Install the following before running the project:

- Python compatible with the installed backend dependencies
- Node.js and npm
- An OpenAI API key with API access and available quota

## 7. Environment Configuration

Create a `.env` file in the project root, alongside `package.json`.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your own API key. Never commit your real `.env` file or publish API credentials.

If the project already has a configured `.env`, preserve its existing values and verify that the required variables are present.

## 8. Installation and Setup

### Step 1: Install frontend dependencies

Open a terminal in the project root:

```powershell
npm install
```

### Step 2: Activate the Python environment

This project uses a root-level `.venv` environment.

From the project root, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the Python executable from the environment directly instead.

### Step 3: Install backend dependencies

With the intended virtual environment active:

```powershell
python -m pip install -r backend/requirements.txt
```

Use the dependency file maintained for the working application.

### Step 4: Verify data and configuration

Ensure the required database, data files, policy documents, and vector-store configuration are available.

If setting up a fresh copy, inspect `backend/load_data.py` and the application's database configuration before running the data loader. Follow the initialization process appropriate for the supplied project data.

## 9. Running the Application

Run the frontend and backend in separate terminals.

### Terminal 1: Start FastAPI

From the project root:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

If the virtual environment is already active, you can omit the activation command.

The API should be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

### Terminal 2: Start React

From the project root:

```powershell
npm run dev
```

Open the local URL printed by Vite in the terminal.

## 10. API Usage

**Endpoint:** `POST /api/chat`

**Request body:**

```json
{
  "query": "What is the status of claim CLM300001?"
}
```

**Example response:**

```json
{
  "query": "What is the status of claim CLM300001?",
  "answer": "The status of claim CLM300001 is Under Review.",
  "tools_used": ["get_claim_details"],
  "scope_status": "in_scope"
}
```

The response above illustrates the API structure. The actual answer may contain additional retrieved claim details.

## 11. Example Questions

Try these questions in the chat interface:

1. What is the status of claim CLM300001?
2. Which documents are missing for claim CLM300001?
3. What is the maternity waiting period under Maternity Protect?
4. Which hospital is linked to claim CLM300001?
5. What is the status of claim CLM999999?

These queries exercise claim retrieval, missing-document checks, policy retrieval, hospital lookup, and unknown-claim handling.

## 12. Validation and Test Results

The following scenarios have been manually tested during development:

| Test                      | Observed result                                                    |
| ------------------------- | ------------------------------------------------------------------ |
| Claim lookup              | Returned the claim status                                          |
| Missing-document lookup   | Identified the missing Claim Form                                  |
| Policy question           | Returned a 24-month maternity waiting period for Maternity Protect |
| Hospital lookup           | Returned linked hospital details                                   |
| Unknown claim ID          | Reported that the claim was not found                              |
| Frontend integration      | Displayed actual backend responses in the chat                     |
| Frontend production build | Completed successfully                                             |
| FastAPI endpoint          | Returned HTTP 200 for a valid claim query                          |

These results represent the scenarios tested during development; they are not a claim of complete automated test coverage.

## 13. Build the Frontend

To create a production build, run from the project root:

```powershell
npm run build
```

Vite generates the production assets in the `dist/` directory.

## 14. Limitations and Future Improvements

- The supplied data and policy documents are synthetic demonstration data.
- Policy answers depend on the content available in the supplied documents.
- The assistant is a prototype and does not make authoritative insurance coverage or claim-settlement decisions.
- Additional automated evaluation, retrieval-quality testing, and broader error-handling tests would improve reliability.
- Production deployment would require appropriate authentication, authorization, privacy controls, monitoring, and security review.

## 15. Conclusion

The Enterprise Insurance Claims & Policy Intelligence Assistant demonstrates how conversational AI, tool calling, structured data retrieval, hybrid search, and RAG can work together in an insurance information application.

The project provides a foundation for exploring grounded question answering across policy documents and claim-related records through a web interface.
