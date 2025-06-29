import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from settings import settings

# Initialize the async instructor client using the OpenAI API key.
instructor_async_client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))

# Updated system prompt for pediatric medical advice
DEFAULT_SYSTEM_PROMPT = """
You are a dedicated 24/7 AI Pediatric Medical Assistant. Your expertise is strictly limited to providing medically relevant guidance for patients aged 0-18 years old.
Your role is to offer clear, concise, and professional advice on common pediatric conditions such as cough, fever, cold, and other age-related symptoms.

When responding:
- Provide a priority level 3 diagnostic response with immediate and clear guidance.
- Ensure all advice is specific to pediatric care; do not provide any information relevant to adult patients.
- If the query is unclear or the provided information is insufficient, respond empathetically with a message like:
  "I'm sorry, but based on the information provided, I recommend that you consult with a doctor within the next 1-2 hours. 
   In the meantime, here are some general precautions you might consider: [list precautions]."

Always maintain a caring, professional tone and strictly focus on medical-related information for children.
"""

def build_message(conversation_history: list[dict], query: str):
    messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}] + conversation_history + [
        {"role": "user", "content": query}
    ]
    return messages

class UserResponse(BaseModel):
    chain_of_thought: str = Field(
        description="Step-by-step reasoning and analysis of the user's query."
    )
    llm_response: str = Field(
        description="Final response to the user's query in the language of the original query."
    )

async def get_chat_completion_using_instructor(messages: list[dict], model: str):
    response: UserResponse = await instructor_async_client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0,
        response_model=UserResponse,
        max_retries=2,
        seed=42
    )
    return response.llm_response

async def respond_to_user_query(query: str):
    messages = build_message([], query)
    answer = await get_chat_completion_using_instructor(messages, "gpt-4o")
    return answer
