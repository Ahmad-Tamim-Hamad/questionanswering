from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangChain setup
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant specialized in answering general and technical questions."),
    ("human", "{question}")
])
chain = LLMChain(llm=llm, prompt=prompt)

# FastAPI setup
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QuestionRequest(BaseModel):
    question: str

# Response model
class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    question = req.question.strip()

    if not question:
        return {"answer": "No question provided."}
    if len(question) > 500:
        return {"answer": "Question is too long. Please keep it under 500 characters."}

    try:
        answer = chain.run({'question': question}).strip()
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
