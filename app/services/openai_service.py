from openai import AsyncOpenAI
from typing import List
import os
from fastapi import HTTPException
from app.utils.logger import log_info, log_success, log_error

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    log_error("OpenAI API key not found!")
    raise HTTPException(
        status_code=500,
        detail="OpenAI API key not found. Please set OPENAI_API_KEY in .env file"
    )

client = AsyncOpenAI(api_key=api_key)

async def generate_questions(topic: str) -> List[str]:
    log_info(f"Generating questions for topic: {topic}")
    
    try:
        prompt = f"Generate 5 research questions about the following topic: {topic}"
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        
        questions = response.choices[0].message.content.strip().split("\n")
        questions = [q.strip("1234567890. ") for q in questions if q.strip()]
        
        log_success(f"Generated {len(questions)} questions successfully")
        return questions
    except Exception as e:
        log_error(f"Error generating questions: {str(e)}")
        raise

async def refine_answers(raw_answers: List[str]) -> List[str]:
    log_info("Refining answers using OpenAI")
    refined_answers = []
    
    try:
        for i, answer in enumerate(raw_answers, 1):
            log_info(f"Refining answer {i}/{len(raw_answers)}")
            prompt = f"Refine and improve the following answer, making it more concise and clear: {answer}"
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            refined_answers.append(response.choices[0].message.content.strip())
        
        log_success("Successfully refined all answers")
        return refined_answers
    except Exception as e:
        log_error(f"Error refining answers: {str(e)}")
        raise

async def generate_summary(answers: List[str]) -> str:
    log_info("Generating summary from answers")
    
    try:
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
        
        summary = response.choices[0].message.content.strip()
        log_success("Summary generated successfully")
        return summary
    except Exception as e:
        log_error(f"Error generating summary: {str(e)}")
        raise