import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from settings import settings

instructor_async_client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))

DEFAULT_SYSTEM_PROMPT = """
You are a world class AI Health Assistant.You will be assisting the user in their health queries.
The user will ask you health related queries. You need to provide them with the best possible answers.
"""


def build_message(conversation_history: list[dict], query: str):
    messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}] + conversation_history + [
        {"role": "user", "content": query}]
    return messages


class UserResponse(BaseModel):
    chain_of_thought: str = Field(description="Think step by step. Analyse the User Query. "
                                              "Provide LLM reasoning for the Query to respond the User")
    llm_response: str = Field(description="LLM Response to the User Query in the language of the user Query")


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

    answer = await get_chat_completion_using_instructor(messages, "gpt-3.5-turbo")

    return answer
