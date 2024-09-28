from openai import OpenAI

def generate_xml(client: OpenAI, pcc_manual: str, pcc_fields_description: str, xml_example: str, history: list) -> str:
    """
    Generates an XML document based on the user's tax-related information.

    Args:
        client (OpenAI): An instance of the OpenAI API client.
        pcc_manual (str): Instruction manual for filling the PCC form.
        pcc_fields_description (str): Description of XML fields for the PCC form.
        xml_example (str): Example XML format for the PCC form.
        history (list): A list containing the conversation history.

    Returns:
        str: Generated XML string with the user's data.
    """
    
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
