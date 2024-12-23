from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.main import templates
from app.services.openai_service import generate_questions, refine_answers, generate_summary
from app.services.tavil_service import fetch_answers
from typing import List
from pydantic import BaseModel

router = APIRouter()

class TopicRequest(BaseModel):
    topic: str

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-questions")
async def generate_research_questions(request: TopicRequest) -> List[str]:
    questions = await generate_questions(request.topic)
    return questions

@router.post("/fetch-answers")
async def get_answers(questions: List[str]) -> List[str]:
    raw_answers = await fetch_answers(questions)
    refined_answers = await refine_answers(raw_answers)
    return refined_answers

@router.post("/generate-summary")
async def get_summary(answers: List[str]) -> str:
    summary = await generate_summary(answers)
    return summary 