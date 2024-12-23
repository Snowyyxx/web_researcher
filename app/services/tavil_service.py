from typing import List
from tavily import TavilyClient
import os
from fastapi import HTTPException

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise HTTPException(
        status_code=500,
        detail="Tavily API key not found. Please set TAVILY_API_KEY in .env file"
    )

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

async def fetch_answers(questions: List[str]) -> List[str]:
    answers = []
    
    for question in questions:
        try:
            # Using qna_search for direct answers to questions
            answer = tavily_client.qna_search(query=question)
            answers.append(answer if answer else "No answer found")
        except Exception as e:
            print(f"Error fetching answer for question '{question}': {str(e)}")
            answers.append("Error fetching answer")
    
    return answers 