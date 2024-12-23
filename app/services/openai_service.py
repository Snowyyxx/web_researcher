from openai import AsyncOpenAI
from typing import List
import os
from fastapi import HTTPException

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise HTTPException(
        status_code=500,
        detail="OpenAI API key not found. Please set OPENAI_API_KEY in .env file"
    )

client = AsyncOpenAI(api_key=api_key)

async def generate_questions(topic: str) -> List[str]:
    prompt = f"Generate 5 research questions about the following topic: {topic}"
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    
    # Parse the response to extract questions
    questions = response.choices[0].message.content.strip().split("\n")
    return [q.strip("1234567890. ") for q in questions if q.strip()]

async def refine_answers(raw_answers: List[str]) -> List[str]:
    refined_answers = []
    
    for answer in raw_answers:
        prompt = f"Refine and improve the following answer, making it more concise and clear: {answer}"
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        
        refined_answers.append(response.choices[0].message.content.strip())
    
    return refined_answers 

async def generate_summary(answers: List[str]) -> str:
    # Combine all answers into one text
    combined_answers = "\n\n".join(answers)
    
    prompt = f"""Based on the following research answers, provide a comprehensive summary:

Answers:
{combined_answers}

Please provide a clear, concise summary that connects the key points from all these answers."""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()