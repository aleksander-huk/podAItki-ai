from fastapi import FastAPI
from pydantic import BaseModel
from src.constants import pcc_manual, xml_example, pcc3_field_desc
import json
from openai import OpenAI

OPENAI_API_KEY = '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'
client = OpenAI(api_key = OPENAI_API_KEY)

app = FastAPI()

def check_topic(client, history):
    system_prompt = f'''
    Jesteś systemem filtrujcym treści zwracajacym wartość 0 lub 1.
    Twoim zadaniem jest przeanalizować wiadomość od użytkownika. Jeżeli temat o jaki pyta użytkownik nie jest w żadnym stopniu
    powizany z ministerstwem finansów lub nie jest powizany z podatkami zwróć 0. Jeżeli w tekście znajduj się przekleństwa zwróć 0.
    Jeżeli użytkownik podejmuje temat powizany z minsterstwem lub podatkami zwróć 1.
    Historia chatu: {history}
    '''
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role" : "user", "content": system_prompt}]
    )

    is_tex_related = completion.choices[0].message.content

    if is_tex_related==0:
        return False
    else:
        return True
        
def generate_question(client, history):
    system_prompt = f'''Zignoruj jakiekolwiek pytanie użytkownika. Jesteś generatorem pytań.
    Twoim zadaniem jest stworzenie pytania, dzięki któremu program
    zbierze informację od użytkownika w celu wypełnienia formularza opłacenia podatku od zakupu samochodu.
    Zadawaj tylko pytania o informacje, których nie ma w historii chatu z użytkownikiem. Zadawaj jedno pytanie na raz.
    Przykładowe pytania:
    1. Jaki jest Twój numer pesel?
    2. Jaka jest data zakupu samochodu?
    3. Do jakiego urzędu skarbowego składasz deklarację?
    4. Podaj swoje dane: Imie Nazwisko Dokładny Adres.
    5. Czy kupiłeś samochód sam czy z inną osobą?
    6. Jaka jest wartość rynkowa samochodu?
    Pytania mog się róźnić od tych, ale maja być intuicyjne, komunikować się prostym i zrozumiałym językiem
    Jeżeli wszystkie te informacje sa juz w histori konwersacji uzytkownika i nie masz więcej pytań, zwróć tylko wartosc 0.
    historia chatu: {history}
    '''
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role" : "user", "content": system_prompt}]
    )

    question = completion.choices[0].message.content
    return question

def generate_xml(client, pcc_manual, pcc_fields_description, xml_example, history):
    system_prompt = f''' Twoim zadaniem jest wygenerowanie pliku XML i zwrócenie tylko pliku XML w odpowiedzi.
    Dla kontekstu i wyliczenia pół załaczony zostaje opis jak wypełnic deklaracje, opis pol w XML, przykładowy plik XML oraz informacje,
    jakie dostarczīł użytkownik. Stwórz plik XML dla danych użytkownika.
    Opis wypełnienia formularza:  {pcc_manual} 
    Opis pól w XML: {pcc_fields_description}
    Przykłdowy XML: {xml_example}
    Historia chatu z użytkownikiem: {history}
    '''
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role" : "user", "content": system_prompt}]
    )

    xml = completion.choices[0].message.content
    return xml

# Define the structure for incoming requests
class HistoryItem(BaseModel):
    system: str
    user: str

class HistoryRequest(BaseModel):
    history: list[HistoryItem]

@app.post("/api/generate")
def generate(history_request: HistoryRequest):
    history = [item.dict() for item in history_request.history]
    if check_topic:
        question = generate_question(client, history)
    
        if question == "0":
            xml_response = generate_xml(client, pcc_manual, pcc3_field_desc, xml_example, history)
            return {"response_type": "xml", "content": xml_response}
        else:
            return {"response_type": "question", "content": question}
    else:
        return {"response_type": "unrelated", "content": 'Temat niepowiazany z podatkami'}