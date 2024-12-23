from typing import List
from tavily import TavilyClient
import os
from fastapi import HTTPException
from app.utils.logger import log_info, log_success, log_error

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    log_error("Tavily API key not found!")
    raise HTTPException(
        status_code=500,
        detail="Tavily API key not found. Please set TAVILY_API_KEY in .env file"
    )

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

async def fetch_answers(questions: List[str]) -> List[str]:
    log_info(f"Fetching answers for {len(questions)} questions")
    answers = []
    
    for i, question in enumerate(questions, 1):
        try:
            log_info(f"Searching for answer to question {i}/{len(questions)}: {question[:50]}...")
            answer = tavily_client.qna_search(query=question)
            answers.append(answer if answer else "No answer found")
            log_success(f"Answer found for question {i}")
        except Exception as e:
            log_error(f"Error fetching answer for question {i}: {str(e)}")
            answers.append("Error fetching answer")
    
    if answers:
        log_success(f"Successfully fetched {len(answers)} answers")
    return answers 