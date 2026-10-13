# Enterprise Insurance Claims & Policy Intelligence Assistant

A Gen-AI-powered insurance assistant that answers policy questions,
retrieves claim details, checks missing documents, and looks up hospital
information through a conversational interface.

## 1. Project Overview

Insurance information is often spread across structured databases and
lengthy policy documents. Finding the right claim details or policy
conditions manually can take time.

This project combines a React chat interface, a FastAPI backend, a
LangGraph agent, structured database tools, and Retrieval-Augmented
Generation (RAG) to provide relevant, source-grounded responses.

**Project domain:** Insurance\
**Project type:** Individual Gen-AI practice project

## 2. Key Features

-   **Policy question answering:** Retrieves relevant policy passages
    using hybrid search and reranking.
-   **Claim lookup:** Retrieves claim status, amounts, and available
    claim details.
-   **Missing-document detection:** Identifies documents marked as
    missing for a specific claim.
-   **Hospital lookup:** Retrieves hospital information linked to a
    claim when available.
-   **LLM tool calling:** Uses a LangGraph agent to select the
    appropriate tools for supported questions.
-   **Scope validation:** Handles greetings and redirects or declines
    unrelated requests.
-   **Interactive chat:** Provides message history, suggested questions,
    loading feedback, and error messages.
-   **API error handling:** Returns safe error responses when unexpected
    processing failures occur.

## 3. Technology Stack

  -----------------------------------------------------------------------
  Component                Technologies
  ------------------------ ----------------------------------------------
  Frontend                 React, Vite, JavaScript

  Backend API              Python, FastAPI, Uvicorn

  Agent orchestration      LangGraph, LangChain

  Language model           OpenAI API

  Structured data          SQLite, SQLAlchemy

  Vector database          ChromaDB

  Embeddings and reranking sentence-transformers

  Hybrid retrieval         Semantic search, BM25, Reciprocal Rank Fusion

  Validation               Pydantic
  -----------------------------------------------------------------------

## 4. System Architecture

1.  The user submits a question through the React chat interface.
2.  The frontend sends a POST request to the FastAPI `/api/chat`
    endpoint.
3.  The LangGraph agent validates the request and determines whether it
    is within scope.
4.  The model selects an appropriate tool when necessary.
5.  The tools retrieve claim, document, or hospital information from
    structured data, or search policy documents using the RAG pipeline.
6.  The agent generates a response based on the retrieved information.
7.  FastAPI returns the result to React, where the answer appears in the
    chat.

**Architecture flow:**

React + Vite → FastAPI → LangGraph Agent → Tools → SQLite / Policy RAG →
Response

## 5. Project Structure

``` text
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

The structure above summarizes the main application components.
Supporting scripts, configuration files, and data files may also be
present.

## 6. Prerequisites

Install the following before running the project:

-   Python compatible with the installed backend dependencies
-   Node.js and npm
-   An OpenAI API key with API access and available quota

## 7. Environment Configuration

Create a `.env` file in the project root, alongside `package.json`.

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your own API key. Never commit your real
`.env` file or publish API credentials.

If the project already has a configured `.env`, preserve its existing
values and verify that the required variables are present.

## 8. Installation and Setup

### Step 1: Install frontend dependencies

Open a terminal in the project root:

``` powershell
npm install
```

### Step 2: Activate the Python environment

This project uses a root-level `.venv` environment.

From the project root, run:

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the Python executable from the
environment directly instead.

### Step 3: Install backend dependencies

With the intended virtual environment active:

``` powershell
python -m pip install -r backend/requirements.txt
```

Use the dependency file maintained for the working application.

### Step 4: Verify data and configuration

Ensure the required database, data files, policy documents, and
vector-store configuration are available.

If setting up a fresh copy, inspect `backend/load_data.py` and the
application's database configuration before running the data loader.
Follow the initialization process appropriate for the supplied project
data.

## 9. Running the Application

Run the frontend and backend in separate terminals.

### Terminal 1: Start FastAPI

From the project root:

``` powershell
cd backend
..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

If the virtual environment is already active, you can omit the
activation command.

The API should be available at:

-   API base URL: `http://127.0.0.1:8000`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`

### Terminal 2: Start React

From the project root:

``` powershell
npm run dev
```

Open the local URL printed by Vite in the terminal.

## 10. API Usage

**Endpoint:** `POST /api/chat`

**Request body:**

``` json
{
  "query": "What is the status of claim CLM300001?"
}
```

**Example response:**

``` json
{
  "query": "What is the status of claim CLM300001?",
  "answer": "The status of claim CLM300001 is Under Review.",
  "tools_used": ["get_claim_details"],
  "scope_status": "in_scope"
}
```

The response above illustrates the API structure. The actual answer may
contain additional retrieved claim details.

### Interaction analytics endpoint

**Endpoint:** `GET /api/analytics/interactions`

This endpoint returns SQL-aggregated interaction statistics, including
totals and breakdowns by channel, intent, sentiment, and resolution
status. Open `http://127.0.0.1:8000/docs` while the backend is running
to inspect and try the endpoint.

## 11. Example Questions

Try these questions in the chat interface:

1.  What is the status of claim CLM300001?
2.  Which documents are missing for claim CLM300001?
3.  What is the maternity waiting period under Maternity Protect?
4.  Which hospital is linked to claim CLM300001?
5.  What is the status of claim CLM999999?

These queries exercise claim retrieval, missing-document checks, policy
retrieval, hospital lookup, and unknown-claim handling.

## 12. Validation and Test Results

The project was validated with automated regression tests, configured
policy-evaluation cases, and API smoke tests.

### Automated regression tests

The discovered pytest suite completed successfully:

-   **12/12 regression tests passed**
-   Coverage includes claim analysis, follow-up scope handling, scope
    validation, missing-document questions, and safe chat error
    handling.
-   One non-blocking Chroma deprecation warning was reported during
    testing.

Run the tests from the `backend/` directory with the project's virtual
environment activated:

``` powershell
python -m pytest -q -ra
```

> The result above reflects the 12 tests discovered by pytest in the
> current project setup; it does not mean every standalone test script
> in the repository was automatically executed.

### Policy-answer evaluation

The configured evaluation runner completed **5/5 checks (100% of the
configured cases)**:

  -----------------------------------------------------------------------
  Evaluation case                     Expected behavior checked
  ----------------------------------- -----------------------------------
  Health Secure Plus                  States the 24-month maternity
                                      waiting period

  Family Care Gold                    Describes the documented
                                      dental-treatment
                                      limitation/accident exception

  Critical Care Elite                 States maternity is not covered
                                      under the base critical illness
                                      plan

  Motor Protect Comprehensive         Identifies the drunk-driving
                                      exclusion

  Global Travel Secure                Explains that known pre-existing
                                      conditions are generally excluded
                                      unless specifically covered
  -----------------------------------------------------------------------

Run the evaluation from `backend/`:

``` powershell
python -m evaluation.run_evaluation
```

The runner writes its report to
`backend/evaluation/evaluation_report.json`.

**Evaluation limitation:** these are configured text-pattern/fact
checks. A 5/5 result does not independently prove complete factual
accuracy, source grounding, or production readiness.

### API smoke tests

The following behaviors were verified during development:

  -----------------------------------------------------------------------
  Test                                Observed result
  ----------------------------------- -----------------------------------
  `POST /api/chat` policy question    Returned a policy-specific answer
                                      for Critical Care Elite with
                                      `scope_status: in_scope` and
                                      `search_policy` listed in
                                      `tools_used`

  `GET /api/analytics/interactions`   Returned HTTP 200 with interaction
                                      summary data

  Interaction analytics               Returned totals and breakdowns for
                                      channel, intent, sentiment, and
                                      resolution status

  Claim lookup                        Returned claim details/status for a
                                      known claim

  Missing-document lookup             Identified the missing Claim Form
                                      for the tested claim

  Policy RAG                          Retrieved the configured maternity
                                      waiting period for Maternity
                                      Protect

  Unknown claim ID                    Reported that the claim was not
                                      found

  Frontend integration                Displayed backend responses in the
                                      chat interface

  Frontend production build           Completed successfully during
                                      development
  -----------------------------------------------------------------------

### Interaction analytics

The optional analytics endpoint is:

``` http
GET /api/analytics/interactions
```

It aggregates the supplied `customer_interactions.csv` records using SQL
and reports totals and breakdowns by channel, intent, sentiment, and
resolution status. The current dataset contains **180,000 interaction
records**. Analytics is an additional project capability; the core
assistant workflows remain claim lookup, missing-document checks,
hospital lookup, and policy-document question answering.

## 13. Build the Frontend

To create a production build, run from the project root:

``` powershell
npm run build
```

Vite generates the production assets in the `dist/` directory.

## 14. Limitations and Future Improvements

-   The supplied data and policy documents are synthetic demonstration
    data.
-   Policy answers depend on the content available in the supplied
    documents.
-   The assistant is a prototype and does not make authoritative
    insurance coverage or claim-settlement decisions.
-   The current evaluation suite contains five configured policy cases
    and uses text-pattern checks; expand it with
    semantic/source-grounding assertions and more varied questions.
-   Continue expanding automated error-handling, retrieval-quality, and
    regression coverage.
-   Production deployment would require appropriate authentication,
    authorization, privacy controls, monitoring, and security review.

## 15. Conclusion

The Enterprise Insurance Claims & Policy Intelligence Assistant
demonstrates how conversational AI, tool calling, structured data
retrieval, hybrid search, and RAG can work together in an insurance
information application.

The project provides a foundation for exploring grounded question
answering across policy documents and claim-related records through a
web interface.
