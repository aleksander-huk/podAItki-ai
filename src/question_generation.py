from openai import OpenAI

def generate_question(client: OpenAI, history: list) -> str:
    """
    Generates a question to gather missing information for the tax form.

    Args:
        client (OpenAI): An instance of the OpenAI API client.
        history (list): A list containing the conversation history.

    Returns:
        str: Returns the next question to ask or '0' if all required information is gathered.
    """

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
