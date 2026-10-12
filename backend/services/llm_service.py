import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPEN_API_KEY is not set."
        "Please add it to your .env file"
    )

client=OpenAI(
    api_key=api_key
)

MODEL_NAME = "gpt-4o-mini"

def generate_answer(
        query:str,
        context:str
)->str:
    """
    Generate a grounded answer using retrieved policy context.
    The model is instructed to answer only from the supplied context and avoid unsupported insurance information.
    """

    system_prompt="""
you are an insurance policy intelligence assistant.

Your job is to answer the user's question using ONLY the policy information provided in the CONTEXT.

GROUNDING RULES:

1. Use only information explicitly supported by the context.
2. Do not invent policy terms,coverage,limits,waiting periods,exclusions, or conditions.
3. If the context does not contain enough information to answer the question, clearly say that the information is not available in the retrieved policy documents.
4. When multiple policies are relevant, distinguish them clearly.
5. Preserve important conditions such as:
    - add-on requirements
    - waiting periods
    - sub-limits
    - exclusions
    -plan variants
6. Do not combine information from different policies as though they belong to one policy.
7. Keep the answer concise and easy to understand.
8. Mention the relevant policy name when providing policy-specific information.
9. Do not make assumptions about the customer's eligibility or claim outcome unless the context explicitly supports it.

The policy documents are synthetic training/simulation documents.
Do not describe them as real insurance contracts.
"""

    user_prompt=f"""
CONTEXT:
{context}

USER QUESTION:
{query}
"""
    response=client.responses.create(
        model=MODEL_NAME,
        instructions=system_prompt,
        input=user_prompt
    )

    return response.output_text.strip()