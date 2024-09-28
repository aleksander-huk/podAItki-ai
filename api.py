# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.constants import pcc_manual, xml_example, pcc3_field_desc
from src.validation import validate_topic
from src.question_generation import generate_question
from src.xml_generation import generate_xml
from openai import OpenAI

OPENAI_API_KEY = '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'
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# Define the structure for incoming requests
class HistoryItem(BaseModel):
    system: str
    user: str

class HistoryRequest(BaseModel):
    history: list[HistoryItem]

@app.post("/api/generate")
def generate(history_request: HistoryRequest):
    history = [item.dict() for item in history_request.history]
    if validate_topic(client, history) or len(history)>1:
        question = generate_question(client, history)
        
        if question == "0":
            xml_response = generate_xml(client, pcc_manual, pcc3_field_desc, xml_example, history)
            return {"response_type": "xml", "content": xml_response}
        else:
            return {"response_type": "question", "content": question}
    else:
        return {"response_type": "unrelated", "content": 'Temat niepowiązany z podatkami'}