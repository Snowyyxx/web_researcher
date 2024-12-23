from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.main import templates
from app.services.openai_service import generate_questions, refine_answers, generate_summary
from app.services.tavil_service import fetch_answers
from typing import List
from pydantic import BaseModel
from app.utils.logger import log_info, log_success, log_error

router = APIRouter()

class TopicRequest(BaseModel):
    topic: str

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    log_info("Serving home page")
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-questions")
async def generate_research_questions(request: TopicRequest) -> List[str]:
    log_info(f"Received request to generate questions for topic: {request.topic}")
    try:
        questions = await generate_questions(request.topic)
        log_success("Questions generated and sent to client")
        return questions
    except Exception as e:
        log_error(f"Failed to generate questions: {str(e)}")
        raise

@router.post("/fetch-answers")
async def get_answers(questions: List[str]) -> List[str]:
    log_info("Received request to fetch answers")
    try:
        raw_answers = await fetch_answers(questions)
        refined_answers = await refine_answers(raw_answers)
        log_success("Answers fetched, refined, and sent to client")
        return refined_answers
    except Exception as e:
        log_error(f"Failed to fetch/refine answers: {str(e)}")
        raise

@router.post("/generate-summary")
async def get_summary(answers: List[str]) -> str:
    log_info("Received request to generate summary")
    try:
        summary = await generate_summary(answers)
        log_success("Summary generated and sent to client")
        return summary
    except Exception as e:
        log_error(f"Failed to generate summary: {str(e)}")
        raise 