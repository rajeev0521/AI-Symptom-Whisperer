from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .services.chat_service import ChatService
from .services.assessment_service import AssessmentService

app = FastAPI()
chat_service = ChatService()
assessment_service = AssessmentService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat/")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    user_id = data.get("user_id", None)
    return chat_service.process_message(user_message, user_id)

@app.post("/start_session/")
async def start_session(request: Request):
    data = await request.json()
    user_id = data.get("user_id", None)
    return chat_service.start_session(user_id)

@app.post("/end_session/")
async def end_session():
    return chat_service.end_session()

@app.post("/assessment/")
async def assessment_endpoint(request: Request):
    data = await request.json()
    assessment_type = data.get("type", "phq9")
    answers = data.get("answers", [])
    return assessment_service.process_assessment(assessment_type, answers)

@app.get("/")
def read_root():
    return {"message": "AI Mental Health Counselor API. Visit /docs for API documentation."}
