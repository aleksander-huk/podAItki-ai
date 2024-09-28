import os
from fastapi import FastAPI
from pydantic import BaseModel
from src.constants import pcc_manual, xml_example, pcc3_field_desc
from src.validation import validate_topic, is_user_asking
from src.question_generation import generate_questionm, generate_rag_response
from src.xml_generation import generate_xml
from openai import OpenAI

# Fetch the API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()


# Define Pydantic models for incoming request data
class HistoryItem(BaseModel):
    """
    Represents a single history item containing system and user messages.
    
    Attributes:
        system (str): Message from the system.
        user (str): Message from the user.
    """
    system: str
    user: str

class HistoryRequest(BaseModel):
    """
    Represents the overall request containing a list of history items.
    
    Attributes:
        history (list[HistoryItem]): List of HistoryItem objects representing the chat history.
    """
    history: list[HistoryItem]

# Define the main API endpoint for generating responses
@app.post("/api/generate")
def generate(history_request: HistoryRequest):
    """
    Main endpoint to handle incoming requests for generating questions or XML based on the chat history.
    
    Args:
        history_request (HistoryRequest): Contains the user's conversation history.
        
    Returns:
        dict: A dictionary containing the response type (either 'xml', 'question', or 'unrelated') and the generated content.
    """
    # Convert the list of HistoryItem objects into dictionaries
    history = [item.dict() for item in history_request.history]
    
    # Validate if the conversation is tax-related
    if validate_topic(client, history):
        # Validate if user asks a question
        if is_user_asking(client, history[-1]):
            rag_answer = generate_rag_response(client, history[-1], pcc_manual)# Ideally create a RAG system for that
            return {"response_type": "rag", "content": rag_answer + ' Czy chcesz teraz stworzyć XLM aby złoyć wniosek o zapłatę podatku PCC3?'}
        else:
            # Generate a question if the topic is valid
            question = generate_question(client, history, pcc_manual, pcc3_field_desc)
            
            # If all necessary questions have been asked, generate XML
            if question == "0":
                xml_response = generate_xml(client, pcc_manual, pcc3_field_desc, xml_example, history)
                return {"response_type": "xml", "content": xml_response}
            else:
                # Return the next question
                return {"response_type": "question", "content": question}
    else:
        # Return a message if the topic is unrelated to taxes
        return {"response_type": "unrelated", "content": 'Temat niepowiązany z podatkami'}
